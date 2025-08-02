@description('Name of the Azure Databricks workspace')
param workspaceName string = 'databricks-${uniqueString(resourceGroup().id)}'

@description('Location for all resources')
param location string = resourceGroup().location

@description('The pricing tier of workspace')
@allowed([
  'standard'
  'premium'
])
param pricingTier string = 'premium'

@description('The managed resource group ID')
param managedResourceGroupId string = '${subscription().id}/resourceGroups/databricks-rg-${workspaceName}-${uniqueString(workspaceName, resourceGroup().id)}'

@description('Enable Unity Catalog')
param enableUnityCatalog bool = false

@description('Tags for the resources')
param tags object = {
  Environment: 'Development'
  Project: 'SampleDataPrep'
  CreatedBy: 'Bicep'
}

// Create Azure Databricks Workspace
resource databricksWorkspace 'Microsoft.Databricks/workspaces@2023-02-01' = {
  name: workspaceName
  location: location
  tags: tags
  sku: {
    name: pricingTier
  }
  properties: {
    managedResourceGroupId: managedResourceGroupId
    parameters: enableUnityCatalog ? {
      enableNoPublicIp: {
        value: false
      }
      prepareEncryption: {
        value: false
      }
      requireInfrastructureEncryption: {
        value: false
      }
    } : {}
    // Additional properties for Unity Catalog if needed
    publicNetworkAccess: 'Enabled'
    requiredNsgRules: 'AllRules'
  }
}

// Outputs
output workspaceName string = databricksWorkspace.name
output workspaceId string = databricksWorkspace.id
output workspaceUrl string = 'https://${databricksWorkspace.properties.workspaceUrl}/'
output location string = location
output pricingTier string = pricingTier
