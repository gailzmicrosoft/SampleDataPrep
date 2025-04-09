param location string // Location for resources.
param acrName string // Name of the Azure Container Registry, e.g. 'myregistry'
param contextPath string // URL of the GitHub repository, e.g. 'https://github.com/your-repo/your-project.git'
param dockerFilePath string // Path to the Dockerfile in the repository, e.g. 'infra/scripts/dockerfiles/Dockerfile_PsPython'
param dockerImageName string // Name of the Dockerfile, e.g. 'Dockerfile_PsPython_Image'
param identity string // Fully qualified resource ID for the managed identity.

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: acrName
}

resource acrTask 'Microsoft.ContainerRegistry/registries/tasks@2019-04-01' = {
  name: 'buildDockerImageTask'
  location: location
  parent: acr
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity}' : {}
    }
  }
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
        '${acr.properties.loginServer}/${dockerImageName}:latest'
      ]
      isPushEnabled: true
    }
    trigger: {
      sourceTriggers: []
      baseImageTrigger: {
        name: 'defaultBaseimageTrigger'
        status: 'Enabled'
        baseImageTriggerType: 'Runtime'
      }
    }
  }
}

output imageName string = '${acr.properties.loginServer}/${dockerImageName}:latest'
