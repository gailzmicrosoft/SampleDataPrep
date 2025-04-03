targetScope = 'subscription'
//**************************************************************************/
// User input section 
//**************************************************************************/
@minLength(6)
@maxLength(10)
@description('Name of the solution. This is used to generate a short unique hash used in all resources.')
param solutionName string = 'chatbot'

@description('Name of the resource group to be used')
param rgName string 

@description('Deployment Location')
param location string = 'centralus'

@description('Postgresql Server Admin User Name')
param postgreSqlServerAdminUser string = 'chatbotPsqlAdminUser'


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
var postgreSqlServerAdminPassword = 'Chatbotdbpassword123' // Capital and small case letters, special chars, numbers. 8-10 length

var useKeyVault = true
//var authType = 'rbac' // 'keyvault' or 'rbac'
var keyVaultName = '${resourcePrefix}kv'
var databaseType = 'PostgreSQL' 




// container registry name and image name
var containerRegistryName = '${resourcePrefix}acr'
var dockerImageName = 'pythonapiapp' // This image must be built and pushed to the container registry already
var imageVersion = 'latest'
var dockerImageURL = '${containerRegistryName}.azurecr.io/${dockerImageName}:${imageVersion}'
// test images
var dockerImageURL1 = 'docker.io/library/nginx:latest'
var dockerImageURL2 = 'mcr.microsoft.com/azuredocs/aci-helloworld:latest'


/**************************************************************************/
// This is the main resource group for the solution. 
/**************************************************************************/
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: rgName
  location: location
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
module keyvault './core/security/keyvault.bicep' = if (useKeyVault) { 
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
module keyvaulAccess './core/security/keyvault-access.bicep' = if (useKeyVault) {
  name: '${keyVaultName}keyvaultPolicy'
  scope: rg
  dependsOn: [
    keyvault // Ensure keyvault is created before keyvaulAccess
  ]
  params: {
    keyVaultName: keyVaultName
    principalId: userAssignedMid.outputs.managedIdentityOutput.objectId
    permissions: {
      secrets: [
        'get'
        'list'
        'set'
        'delete'
      ]
    }
  }
  
}

/**************************************************************************/
// Create a storage account and a container
/**************************************************************************/
// var initial_blob_containers = [ { name: 'raw' }, { name: 'processed' } ]
// module storageModule './core/storage/storage-account.bicep' = {
//   name: storageAccountName
//   scope: rg
//   params: {
//     name: storageAccountName
//     location: location
//     useKeyVault: useKeyVault
//     allowBlobPublicAccess: false
//     allowSharedKeyAccess: true
//     defaultToOAuthAuthentication: false
//     dnsEndpointType: 'Standard'
//     minimumTlsVersion: 'TLS1_2'
//     networkAcls: {
//       bypass: 'AzureServices'
//       defaultAction: 'Allow'
//     }
//     publicNetworkAccess: 'Enabled'
//     containers: initial_blob_containers
//   }
// }

/*************************************************************************************/
// Create azure database for postgresql server with default database 'postgres'
/*************************************************************************************/
// module postgresDBModule './core/database/postgresdb.bicep' = if (databaseType == 'PostgreSQL') {
//   name: 'deploy_postgres_sql'
//   scope: rg
//   params: {
//     location:location
//     serverName:postgreSqlServerName
//     version: '11'
//     administratorLogin: postgreSqlServerAdminUser
//     administratorLoginPassword: postgreSqlServerAdminPassword
//     additionalDatabase: '' // If it is same as postgres or it is empty, it will not be created. postgres is created by default 
//     serverEdition: 'Burstable'
//     skuSizeGB:32
//     dbInstanceType: 'Standard_B4ms' // available SKUs: B1ms, B2ms, B4ms, B8ms, B16ms
//     availabilityZone: '1' // Not all tiers support availability zones. set to '' for 'Standard_B1ms' may work
//     allowAllIPsFirewall: false
//     allowAzureIPsFirewall: true
//     managedIdentityObjectId: userAssignedMid.outputs.managedIdentityOutput.objectId
//     managedIdentityObjectName: userAssignedMid.outputs.managedIdentityOutput.name
//   }
// }



/**************************************************************************/
// If Use existing PostgreSQL server and other resources created above
/**************************************************************************/
// Reference the existing PostgreSQL server and other resources
// resource postgresDBModule 'Microsoft.DBforPostgreSQL/servers@2022-11-01' existing = {
//   name: 'deploy_postgres_sql'
//   scope: rg
// }


// // Create Container Registry
// module containerregistry './core/host/azurecontainerregistry.bicep' = {
//   name: containerRegistryName
//   scope: rg
//   params: {
//     acrName: containerRegistryName
//     location: location
//   }
// }



/**************************************************************************/
// If Use existing container registry created already somewhere else
/************************************************* *************************/
// If the container registry is created in a different resource group, 
// uncomment the following lines and comment the above lines
// resource acr_rg 'Microsoft.Resources/resourceGroups@2024-03-01' = existing {
//   name: acr_rgName
// }
// resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-12-01-preview' existing = {
//   name: containerRegistryName
//   scope: resourceGroup(acr_rgName)
// }
// output containerRegistryId string = containerRegistry.id


// module logAnalyticsWorkspace './core/monitor/loganalytics.bicep' = {
//   name: logAnalyticsWorkspaceName
//   scope:rg
//   params: {
//     name: logAnalyticsWorkspaceName
//     location: location
//     skuName: 'PerGB2018'
//     tags: {
//       displayName: 'Log Analytics Workspace'
//     }
//   }
// }


// module appInsights './core/monitor/applicationinsights.bicep' = {
//   name: appInsightsName
//   scope: rg
//   params: {
//     name: appInsightsName
//     location: location
//     tags: {
//       displayName: 'Application Insights'
//     }
//     logAnalyticsWorkspaceId: logAnalyticsWorkspace.outputs.id
//   }
  
// }

// module containerAppEnv './core/host/containerappenv.bicep' = {
//   name: containerAppEnvName
//   scope: rg
//   params: {
//     environmentName: containerAppEnvName
//     location: location
//     logAnalyticsWorkspaceObject: {
//       id: logAnalyticsWorkspace.outputs.id
//       customerId: logAnalyticsWorkspace.outputs.customerId
//     }
//   }
// }


/**************************************************************************/
// Some environment variables for the container app
/**************************************************************************/
// module containerApp './core/host/containerapp.bicep' = {

// var appEnvironVars = [
//   {
//     name: 'POSTGRESQL_SERVER'
//     value: postgreSqlServerName
//   }
//   {
//     name: 'APP_SITE_NAME'
//     value: 'https://${containerAppName}.azurewebsites.net'
//   }
//   {
//     name: 'APPLICATIONINSIGHTS_INSTRUMENTATION_KEY'
//     value: appInsights.outputs.connectionString
//   }
// ]

// module containerApp './core/host/containerapp.bicep' = {
//   name: containerAppName
//   scope: rg
//   params: {
//     containerAppEnvId: containerAppEnv.outputs.id
//     location: location
//     image: dockerImageURL2 // for testing purposes for now
//     containerAppName: containerAppName
//     containerPort: 8000
//     cpuCores: 1
//     memory: '2.0Gi'
//     minReplicas: 1
//     maxReplicas: 10
//     environmentVariables: appEnvironVars
//     secrets: [] // will need to add them later 
//     containerRegistryName: containerRegistryName
//     userAssignedMidId:userAssignedMid.outputs.id
//   }
// }



// // store the postgresql server name in key vault
// module keyvaultSecretPostgreServerName './core/security/keyvault-secret.bicep' = if (useKeyVault) {
//   name: 'postgresql-server-name'
//   scope: rg
//   dependsOn: [
//     keyvault // Ensure keyvault is created before keyvaultSecret
//   ]
//   params: {
//     name: 'postgresql-server-name'
//     tags: {}
//     keyVaultName: keyVaultName
//     contentType: 'string'
//     secretValue: postgreSqlServerName
//     enabled: true
//     exp: 0 // No expiration time
//     nbf: 0 // Valid immediately
//   }
  
// }
// // store the postgresql server admin user in key vault
// module keyvaultSecretPostgreAdminUser './core/security/keyvault-secret.bicep' = if (useKeyVault) {
//   name: 'postgresql-server-admin-user'
//   scope: rg
//   dependsOn: [
//     keyvault // Ensure keyvault is created before keyvaultSecret
//   ]
//   params: {
//     name: 'postgresql-server-admin-user'
//     tags: {}
//     keyVaultName: keyVaultName
//     contentType: 'string'
//     secretValue: postgreSqlServerAdminUser
//     enabled: true
//     exp: 0 // No expiration time
//     nbf: 0 // Valid immediately
//   }
 
// }
// // store the postgresql server admin password in key vault
// module keyvaultSecretPostgreAdminPassword './core/security/keyvault-secret.bicep' = if (useKeyVault) {
//   name: 'postgresql-server-admin-user-password'
//   scope: rg
//   dependsOn: [
//     keyvault // Ensure keyvault is created before keyvaultSecret
//   ]
//   params: {
//     name: 'postgresql-server-admin-user-password'
//     tags: {}
//     keyVaultName: keyVaultName
//     contentType: 'string'
//     secretValue: postgreSqlServerAdminPassword
//     enabled: true
//     exp: 0 // No expiration time
//     nbf: 0 // Valid immediately
//   }
  
// }



// var posgresqlServerFQN = '${postgreSqlServerName}.postgres.database.azure.com'
// var myBaseURL = 'https://raw.githubusercontent.com/gailzmicrosoft/TestCode/main/infra/'

// // This one has worked 
// module deployPsqlScriptCreateTables './core/database/deploy_psql_create_tables_script.bicep' = if (databaseType == 'PostgreSQL') {
//   name: 'deploy_psql_create_tables_script'
//   scope: rg
//   params: {
//     location: location
//     baseUrl: myBaseURL
//     keyVaultName: keyVaultName
//     postgreSqlServerName: postgreSqlServerName
//     postgresSqlServerFQN: posgresqlServerFQN
//     postgreSqlDbName: 'postgres'
//     adminPrincipalName:postgreSqlServerAdminUser
//     identity:userAssignedMid.outputs.managedIdentityOutput.id
//     identityName: userAssignedMid.outputs.managedIdentityOutput.name
//   }
// }



/**************************************************************************/
// Testing Code Section: Below code are being developed and tested
/**************************************************************************/



// var posgresqlServerFQN = '${postgreSqlServerName}.postgres.database.azure.com'
// var myBaseURL = 'https://raw.githubusercontent.com/gailzmicrosoft/TestCode/main/infra/'

// This modules has not worked in Azure. 
// Azure has issue with pandas library used by Python.
// It is not able to load the library.
// module deployPsqlScriptLoadTables './core/database/deploy_psql_load_tables_script.bicep' = if (databaseType == 'PostgreSQL') {
//   name: 'deploy_psql_load_tables_script'
//   scope: rg
//   params: {
//     location: location
//     baseUrl: myBaseURL
//     keyVaultName: keyVaultName
//     postgreSqlServerName: postgreSqlServerName
//     postgresSqlServerFQN: posgresqlServerFQN
//     postgreSqlDbName: 'postgres'
//     adminPrincipalName:postgreSqlServerAdminUser
//     identity:userAssignedMid.outputs.managedIdentityOutput.id
//     identityName: userAssignedMid.outputs.managedIdentityOutput.name
//   }
// }




// This module has not worked in Azure/
// Issues are that the AzurePowerShell is not able to run az command natively like AzureCLI or pip install natively like AzureCLI.

// module powerShellLoadTables './core/database/deploy_powershell_load_tables_script.bicep' = if (databaseType == 'PostgreSQL') {
//   name: 'powershell_deploy_psql_load_tables_script'
//   scope: rg
//   params: {
//     location: location
//     baseUrl: myBaseURL
//     keyVaultName: keyVaultName
//     postgreSqlServerName: postgreSqlServerName
//     postgresSqlServerFQN: posgresqlServerFQN
//     postgreSqlDbName: 'postgres'
//     adminPrincipalName:postgreSqlServerAdminUser
//     identity:userAssignedMid.outputs.managedIdentityOutput.id
//     identityName: userAssignedMid.outputs.managedIdentityOutput.name
//     acrName: containerRegistryName
//   }
// }



var contextPath = 'https://raw.githubusercontent.com/gailzmicrosoft/TestCode/main/'
var dockerFilePath = 'infra/scripts/dockerfiles/Dockerfile_PsPython'

// 
module registerDockerImage './core/host/_register-docker-image.bicep' = {
  name: 'registerDockerImage'
  scope: rg
  params: {
    location: location
    acrName: containerRegistryName
    contextPath: contextPath
    dockerFilePath: dockerFilePath
    dockerImageName: 'pspythonimage'
    identity: userAssignedMid.outputs.managedIdentityOutput.id
  }
}

