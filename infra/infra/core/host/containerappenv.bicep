@description('Name of the Container App Environment')
param environmentName string

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Log Analytics Workspace Object')
param logAnalyticsWorkspaceObject object


resource containerAppEnv 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: environmentName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspaceObject.customerId
        sharedKey: listKeys(logAnalyticsWorkspaceObject.id, '2021-06-01').primarySharedKey
      }
    }
  }
}

output name string = containerAppEnv.name
output id string = containerAppEnv.id
output location string = containerAppEnv.location
