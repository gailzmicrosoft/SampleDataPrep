// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.


param acrName string 

@description('Provide a location for the registry.')
param location string = resourceGroup().location

@description('Provide a tier of your Azure Container Registry.')
param acrSku string = 'Basic'


param dockerImageName string = 'myapp'
@description('Provide a tag for the Docker image.')

param dockerImageTag string = 'latest'


param contextPath string = 'context'
@description('Provide a path to the Dockerfile.')

param dockerFilePath string = 'Dockerfile'
@description('Provide a name for the Docker image.')

resource acrResource 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: acrSku
  }
  properties: {
    adminUserEnabled: true
  }
}


resource acrTask 'Microsoft.ContainerRegistry/registries/tasks@2019-04-01' = {
  parent: acrResource
  name: 'buildAndPushTaskForDockerImage'
  location: location
  properties: {
    status: 'Enabled'
    platform: {
      os: 'Linux'
      architecture: 'amd64'
    }
    agentConfiguration: {
      cpu: 2
    }
    step: {
      type: 'Docker'
      contextPath: contextPath
      dockerFilePath: dockerFilePath
      imageNames: [
        '${acrResource.name}.azurecr.io/${dockerImageName}:${dockerImageTag}'
      ]
      isPushEnabled: true
    }
  }
}

resource acrTaskRun 'Microsoft.ContainerRegistry/registries/taskRuns@2019-06-01-preview' = {
  parent: acrResource
  name: 'buildAndPushTaskForDocerImageRun'
  location: location
  properties: {
    runRequest: {
      type: 'TaskRunRequest'
      taskId: acrTask.id
    }
  }
}


output acrName string = acrResource.name
output acrId string = acrResource.id
output acrEndpoint string = acrResource.properties.loginServer
