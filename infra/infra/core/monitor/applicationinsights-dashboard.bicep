@description('Creates a dashboard for an Application Insights instance.')
param name string
param location string = resourceGroup().location
param tags object = {}

resource dashboard 'Microsoft.Portal/dashboards@2020-09-01-preview' = {
  name: name
  location: location
  tags: tags
  properties: {
    lenses: [
      {
        order: 0
        parts: [
          {
            position: {
              x: 0
              y: 0
              colSpan: 3
              rowSpan: 2
            }
            metadata: {
              inputs: []
              type: 'Extension/HubsExtension/PartType/MarkdownPart'
              settings: {
                content: {
                  settings: {
                    content: '# Welcome to your new dashboard'
                    title: 'Welcome'
                    subtitle: ''
                  }
                }
              }
            }
          }
        ]
      }
    ]
    metadata: {
      model: {
        timeRange: {
          value: 'last24hours'
          type: 'MsPortalFx.Composition.Configuration.ValueTypes.TimeRange'
        }
        filterLocale: 'en-us'
        filters: {
          MsPortalFx_TimeRange: {
            model: {
              format: 'utc'
              granularity: 'auto'
              relative: {
                duration: 24
                timeUnit: 1
              }
            }
            displayCache: {
              name: 'Last 24 hours'
              value: 'last24hours'
            }
          }
        }
      }
    }
  }
}
