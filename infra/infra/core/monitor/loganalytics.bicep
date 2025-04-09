metadata description = 'Log Analytics workspace.'
param name string
param location string = resourceGroup().location
param tags object = {}
param skuName string = 'PerGB2018'  // accepted values: 'PerGB2018', 'CapacityReservation', 'CapacityReservationV2', 'Free', 'Standby', 'Premium'.
param capacityReservationLevel int = 100

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    sku: skuName == 'CapacityReservation' ? {
      name: skuName
      capacityReservationLevel: capacityReservationLevel
    } : {
      name: skuName
    }
  }
}

output id string = logAnalytics.id
output customerId string = logAnalytics.properties.customerId
output name string = logAnalytics.name
