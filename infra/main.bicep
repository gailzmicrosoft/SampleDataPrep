targetScope = 'subscription'
//**************************************************************************/
// User input section 
//**************************************************************************/
@minLength(6)
@maxLength(10)
@description('Name of the solution. This is used to generate a short unique hash used in all resources.')
param solutionName string = 'chatbot'

@description('Set to true to create the resource group. Set to false if the resource group already exists.')
param createResourceGroup bool = false

@description('Name of the resource group to be used')
param rgName string 

@description('Deployment Location')
param location string = 'centralus' // 'eastus2' // 'eastus' // 'westus2' // 'westeurope' // 'uksouth' // 'centralus' // 'australiaeast'

@description('Postgresql Server Admin User Name')
param postgreSqlServerAdminLogin string = 'chatbotPsqlAdminUser'


/**************************************************************************/
// Resource name generation section
/**************************************************************************/
var resourceTokenRaw = toLower(uniqueString(subscription().id, rgName, solutionName))
var trimmedToken = length(resourceTokenRaw) > 8 ? substring(resourceTokenRaw, 0, 8) : resourceTokenRaw
var resourcePrefixRaw = '${solutionName}${trimmedToken}'
var resourcePrefix =toLower(replace(resourcePrefixRaw, '_', ''))


/**************************************************************************/
// Resource name generation section
/**************************************************************************/

var containerAppEnvName = '${resourcePrefix}env'
var containerAppName = '${resourcePrefix}app'
var rgMidName = '${resourcePrefix}rgMid'
var logAnalyticsWorkspaceName = '${resourcePrefix}law'
var appInsightsName = '${resourcePrefix}appinsights'
var storageAccountName = '${resourcePrefix}storage'
var postgreSqlServerName = '${resourcePrefix}pgserver'
var postgreSqlServerAdminPassword = 'Hybrid-Prototype-Pass-12345!' // Capital and small case letters, special chars, numbers. 8-10 length

var useKeyVault = true
//var authType = 'rbac' // 'keyvault' or 'rbac'
var keyVaultName = '${resourcePrefix}kv'
var databaseType = 'PostgreSQL'
var databaseName = 'postgres' // default database name for PostgreSQL server




// container registry name and image name
var containerRegistryName = '${resourcePrefix}acr'
var dockerImageName = 'chatbottestapp' // This image must be built and pushed to the container registry already
var dockerImageVersion = 'latest'
var dockerImageURL = '${containerRegistryName}.azurecr.io/${dockerImageName}:${dockerImageVersion}'
// test images
var testDockerImageURL = 'docker.io/library/nginx:latest' // 'mcr.microsoft.com/azuredocs/aci-helloworld:latest'


/**************************************************************************/
// This is the main resource group for the solution. 
/**************************************************************************/
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = if (createResourceGroup) {
  name: rgName
  location: location
}

resource existingRg 'Microsoft.Resources/resourceGroups@2024-03-01' existing = if (!createResourceGroup) {
  name: rgName
}


/**************************************************************************/
// Create resource group level managed identity that has the right 
// permissions
/**************************************************************************/

module userAssignedMid './core/security/managed-identity.bicep' = {
  name: rgMidName
  scope: rg
  params: {
    location: location
    miName: rgMidName
  }
}


/**************************************************************************/
// create a key vault and store secrets
/**************************************************************************/
// create a key vault
module keyVault './core/security/keyvault.bicep' = if (useKeyVault) { 
  name: keyVaultName
  scope: rg
  params: {
    name: keyVaultName
    location: location
    principalId: userAssignedMid.outputs.managedIdentityOutput.objectId
    tags: {
      displayName: 'Key Vault for - ${solutionName}'
    }
  }
}
// create a key vault access policy for the managed identity
// to access the key vault
module keyVaultAccess './core/security/keyvault-access.bicep' = if (useKeyVault) {
  name: '${keyVaultName}keyvaultPolicy'
  scope: rg
  dependsOn: [
    keyVault
  ]
  params: {
    keyVaultName: keyVaultName
    principalId: userAssignedMid.outputs.managedIdentityOutput.objectId
    permissions: {
      secrets: [
        'get'
        'set'
        'list'
      ]
    }
  }
  
}

/**************************************************************************/
// Create a storage account and a container
/**************************************************************************/
var initialBlobContainers = [ { name: 'raw' }, { name: 'processed' }, {name: 'results'} ]
module storageModule './core/storage/storage-account.bicep' = {
  name: storageAccountName
  scope: rg
  params: {
    name: storageAccountName
    location: location
    useKeyVault: useKeyVault
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    defaultToOAuthAuthentication: false
    dnsEndpointType: 'Standard'
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
    publicNetworkAccess: 'Enabled'
    containers: initialBlobContainers
  }
}

/*************************************************************************************/
// Create azure database for postgresql server with default database 'postgres'
/*************************************************************************************/
module postgreSqlResource './core/database/postgresdb.bicep' = if (databaseType == 'PostgreSQL') {
  name: 'deployPostgresSqlServerResources'
  scope: rg
  params: {
    location:location
    serverName:postgreSqlServerName
    version: '11'
    administratorLogin: postgreSqlServerAdminLogin
    administratorLoginPassword: postgreSqlServerAdminPassword
    databaseName: databaseName
    serverEdition: 'Burstable'
    skuSizeGB:32
    dbInstanceType: 'Standard_B4ms' // available SKUs: B1ms, B2ms, B4ms, B8ms, B16ms
    availabilityZone: '1' // Not all tiers support availability zones. set to '' for 'Standard_B1ms' may work
    allowAllIPsFirewall: true
    allowAzureIPsFirewall: true
    managedIdentityObjectId: userAssignedMid.outputs.managedIdentityOutput.objectId
    managedIdentityObjectName: userAssignedMid.outputs.managedIdentityOutput.name
  }
}


// store the postgresql server name in key vault
module keyvaultSecretPostgreServerName './core/security/keyvault-secret.bicep' = if (useKeyVault) {
  name: 'kvNameAsPostgreSqlServerName'
  scope: rg
  dependsOn: [
    keyVault // Ensure keyvault is created before keyvaultSecret
  ]
  params: {
    name: 'postgresqlServerName'
    tags: {}
    keyVaultName: keyVaultName
    contentType: 'string'
    secretValue: postgreSqlServerName
    enabled: true
    exp: 0 // No expiration time
    nbf: 0 // Valid immediately
  }
}



// store the postgresql server name in key vault
module keyvaultSecretPostgreServerDbName './core/security/keyvault-secret.bicep' = if (useKeyVault) {
  name: 'kvNameAsPostgreSqlDbName'
  scope: rg
  dependsOn: [
    keyVault // Ensure keyvault is created before keyvaultSecret
  ]
  params: {
    name: 'postgresqlDbName'
    tags: {}
    keyVaultName: keyVaultName
    contentType: 'string'
    secretValue: 'postgres'
    enabled: true
    exp: 0 // No expiration time
    nbf: 0 // Valid immediately
  }
}

// store the postgresql server name in key vault
module keyvaultSecretPostgreServerEndPoint './core/security/keyvault-secret.bicep' = if (useKeyVault) {
  name: 'kvNameAsPostgreSqlEndPoint'
  scope: rg
  dependsOn: [
    keyVault // Ensure keyvault is created before keyvaultSecret
  ]
  params: {
    name: 'postgresqlEndPoint'
    tags: {}
    keyVaultName: keyVaultName
    contentType: 'string'
    secretValue: postgreSqlServerName
    enabled: true
    exp: 0 // No expiration time
    nbf: 0 // Valid immediately
  }
}


// store the postgresql server admin user in key vault
module keyvaultSecretPostgreAdminUser './core/security/keyvault-secret.bicep' = if (useKeyVault) {
  name: 'kvNameAsPostgreSqlAdminLogin'
  scope: rg
  dependsOn: [
    keyVault // Ensure keyvault is created before keyvaultSecret
  ]
  params: {
    name: 'postgresqlAdminLogin'
    tags: {}
    keyVaultName: keyVaultName
    contentType: 'string'
    secretValue: postgreSqlServerAdminLogin
    enabled: true
    exp: 0 // No expiration time
    nbf: 0 // Valid immediately
  }
 
}
// store the postgresql server admin password in key vault
module keyvaultSecretPostgreAdminPassword './core/security/keyvault-secret.bicep' = if (useKeyVault) {
  name: 'kvNameAsPostgreSqlServerAdminPassword'
  scope: rg
  dependsOn: [
    keyVault // Ensure keyvault is created before keyvaultSecret
  ]
  params: {
    name: 'postgresqlAdminPassword'
    tags: {}
    keyVaultName: keyVaultName
    contentType: 'string'
    secretValue: postgreSqlServerAdminPassword
    enabled: true
    exp: 0 // No expiration time
    nbf: 0 // Valid immediately
  }
  
}


/**************************************************************************/
// If Use existing PostgreSQL server and other resources created above
/**************************************************************************/
// // Reference the existing PostgreSQL server and other resources
// resource posgreSqlResource 'Microsoft.DBforPostgreSQL/servers@2022-11-01' existing = {
//   name: 'deploy_postgres_sql'
//   scope: rg
// }




// Create Container Registry
module containerregistry './core/host/azurecontainerregistry.bicep' = {
  name: containerRegistryName
  scope: rg
  params: {
    acrName: containerRegistryName
    location: location
  }
}



// // Create Container Registry
// module acrResource './core/host/azurecontainerregistry_with_tasks.bicep' = {
//   name: containerRegistryName
//   scope: rg
//   params: {
//     acrName: containerRegistryName
//     location: location
//   }
// }


// // var contextPath = 'https://github.com/gailzmicrosoft/TestCode'
// // var dockerFilePath = 'Dockerfile_testapp'

// var contextPath = 'https://github.com/gailzmicrosoft/TestCode'
// var dockerFilePath = 'src/testapp/Dockerfile_testapp'

// module acrTask './core/host/azurecontainerregistry_with_tasks.bicep' = {
//   name: 'buildAndPushTask'
//   scope: rg
//   params: {
//     // acrName: containerRegistryName
//     // location: location
//     acrName: acrResource.outputs.acrName
//     dockerImageName: dockerImageName
//     dockerImageTag: dockerImageVersion
//     contextPath: contextPath
//     dockerFilePath: dockerFilePath
//   }
// }

// module acrTaskRun './core/host/azurecontainerregistry_with_tasks.bicep' = {
//   name: 'buildAndPushTaskRun'
//   scope: rg
//   params: {
//     acrName: acrResource.outputs.acrName
//     location: location
//   }
//   dependsOn: [
//     acrTask
//   ]
// }






module logAnalyticsWorkspace './core/monitor/loganalytics.bicep' = {
  name: logAnalyticsWorkspaceName
  scope:rg
  params: {
    name: logAnalyticsWorkspaceName
    location: location
    skuName: 'PerGB2018'
    tags: {
      displayName: 'Log Analytics Workspace'
    }
  }
}


module appInsights './core/monitor/applicationinsights.bicep' = {
  name: appInsightsName
  scope: rg
  params: {
    name: appInsightsName
    location: location
    tags: {
      displayName: 'Application Insights'
    }
    logAnalyticsWorkspaceId: logAnalyticsWorkspace.outputs.id
  }
  
}

module containerAppEnv './core/host/containerappenv.bicep' = {
  name: containerAppEnvName
  scope: rg
  params: {
    environmentName: containerAppEnvName
    location: location
    logAnalyticsWorkspaceObject: {
      id: logAnalyticsWorkspace.outputs.id
      customerId: logAnalyticsWorkspace.outputs.customerId
    }
  }
}


/**************************************************************************/
// Some environment variables for the container app
/**************************************************************************/
// module containerApp './core/host/containerapp.bicep' = {

var appEnvironVars = [
  {
    name: 'POSTGRESQL_SERVER'
    value: postgreSqlServerName
  }
  {
    name: 'KEY_VAULT_NAME'
    value: keyVaultName
  }
  {
    name: 'APP_SITE_NAME'
    value: 'https://${containerAppName}.azurewebsites.net'
  }
  {
    name: 'APPLICATIONINSIGHTS_INSTRUMENTATION_KEY'
    value: appInsights.outputs.connectionString
  }
]



// Secret name must consist of lower case alphanumeric characters, '-', and must start and end with an alphanumeric character. 
var appSecrets = [
  {
    name: 'key-vault-name'
    value: keyVaultName
  }
  {
    name: 'postgresql-end-point'
    value: postgreSqlResource.outputs.postgreSqlDetails.endPoint
  }
  {
    name: 'postgreql-db-name'
    value: postgreSqlResource.outputs.postgreSqlDetails.dBName
  }
]

module containerApp './core/host/containerapp.bicep' = {
  name: containerAppName
  scope: rg
  params: {
    containerAppEnvId: containerAppEnv.outputs.id
    location: location
    image: testDockerImageURL // for testing purposes for now
    //image: dockerImageURL // test the docker image just built in this BICEP code  
    containerAppName: containerAppName
    containerPort: 8000
    cpuCores: 1
    memory: '2.0Gi'
    minReplicas: 1
    maxReplicas: 10
    environmentVariables: appEnvironVars
    secrets: appSecrets 
    containerRegistryName: containerRegistryName
    userAssignedMidId:userAssignedMid.outputs.id
  }
  dependsOn: [
    keyVaultAccess
    keyVault
    //acrTaskRun
  ]
}


var myBaseURL = 'https://raw.githubusercontent.com/gailzmicrosoft/TestCode/main/'

module deployPsqlScriptCreateTables './core/database/psql_create_tables_script.bicep' = if (databaseType == 'PostgreSQL') {
  name: 'main_deploy_psql_create_tables_script'
  scope: rg
  params: {
    location: location
    baseUrl: myBaseURL
    postgreSqlServerName: postgreSqlResource.outputs.serverName
    postgresSqlEndPoint: postgreSqlResource.outputs.endPoint
    postgreSqlDbName: postgreSqlResource.outputs.dBName
    adminPrincipalName: postgreSqlResource.outputs.adminLogin
    identity:userAssignedMid.outputs.managedIdentityOutput.id
    identityName: userAssignedMid.outputs.managedIdentityOutput.name
  }
}

