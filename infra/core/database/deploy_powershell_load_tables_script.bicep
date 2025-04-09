@description('Specifies the location for resources.')
param location string
param baseUrl string
param keyVaultName string 
param postgreSqlServerName string // Name of the PostgreSQL server, e.g. 'myserver'
param postgresSqlEndPoint string // fully qualified server name, e.g. 'myserver.postgres.database.azure.com'
param postgreSqlDbName string // Name of the PostgreSQL database, e.g. 'mydb'
param adminPrincipalName string
param identity string // Fully qualified resource ID for the managed identity. 
param identityName string // Name of the managed identity



var myArguments = '-baseUrl "${baseUrl}" -resourceGroup "${resourceGroup().name}" -key_vault_name "${keyVaultName}" -postgres_server_name "${postgreSqlServerName}" -host_name "${postgresSqlEndPoint}" -database_name "${postgreSqlDbName}" -admin_principal_name "${adminPrincipalName}" -identity_name "${identityName}"'

// limitation 1 AzurePowerShell can not run az command natively like AzureCLI.
// limitation 2 AzurePowerShell can not run pip install natively like AzureCLI.
// This method can not be used for complicated scripts that need to run az command or pip install.
var myPsUri = '${baseUrl}infra/scripts/run_python_load_tables.ps1'
resource runPowerShellScript 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: 'RunSimplePowerShellScript'
  location: location
  identity: {
        type: 'UserAssigned'
        userAssignedIdentities: {
          '${identity}' : {}
        }
      }
  kind: 'AzurePowerShell'
  properties: {
    primaryScriptUri: myPsUri
    arguments: myArguments
    azPowerShellVersion: '7.4.0'
    cleanupPreference: 'Always'
    retentionInterval: 'PT1H'
  }
}
