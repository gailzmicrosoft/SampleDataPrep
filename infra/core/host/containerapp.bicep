@description('Container App Environment ID')
param containerAppEnvId string

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Docker image to deploy')
param image string = 'mcr.microsoft.com/azuredocs/aci-helloworld:latest'

@description('Name of the Container App')
param containerAppName string

@description('Port the container listens on')
param containerPort int

@description('CPU cores allocated to the container')
param cpuCores int = 1

@description('Memory allocated to the container')
param memory string = '2.0Gi'

@description('Minimum number of container replicas')
param minReplicas int = 1

@description('Maximum number of container replicas')
param maxReplicas int = 10

@description('Environment variables for the container')
param environmentVariables array = []

@description('Secrets for the container')
param secrets array = []

@description('Container Registry Name')
param containerRegistryName string

@description('Managed Identity ID for ACR')
param userAssignedMidId string

// @description('Managed Identity Namme for ACR')
// param userAssignedMidName string

resource containerApp 'Microsoft.App/containerApps@2022-03-01' = {
  name: containerAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedMidId}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppEnvId
    configuration: {
      ingress: {
        external: true
        targetPort: containerPort
      }
      registries: [
        {
          server: '${containerRegistryName}.azurecr.io'
          identity: userAssignedMidId
        }
      ]
      secrets: secrets
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: image
          resources: {
            cpu: cpuCores
            memory: memory
          }
          env: environmentVariables
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
}

output name string = containerApp.name
output id string = containerApp.id
output location string = containerApp.location
output environmentId string = containerApp.properties.managedEnvironmentId
output containerAppUrl string = 'https://${containerAppName}.${location}.azurecontainerapps.io'
