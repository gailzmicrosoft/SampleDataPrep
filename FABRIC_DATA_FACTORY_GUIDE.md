# Microsoft Fabric Data Factory: SQL to Bronze Layer Data Flow Guide

## Overview
This guide provides comprehensive instructions for using **Microsoft Fabric Data Factory Data Flows** to copy sample data from Gaiye-SQL-DB (SalesLT schema) to your retail solution bronze layer. This approach is enterprise-grade, scalable, and provides better monitoring and error handling than notebook-based solutions.

## Why Use Data Factory Data Flows?

### ✅ **Advantages over Notebook Approach:**
- **Visual Interface**: Drag-and-drop pipeline creation
- **Enterprise Scale**: Handle large datasets efficiently
- **Built-in Monitoring**: Real-time execution tracking and logging
- **Error Handling**: Automatic retry logic and failure notifications
- **Security**: Integrated authentication and data encryption
- **Performance**: Optimized for large-scale data movement
- **Scheduling**: Built-in job scheduling and triggers
- **Lineage Tracking**: Complete data lineage and impact analysis

---

## Step-by-Step Implementation Guide

### **Step 1: Create Data Factory Pipeline**

1. **Navigate to Data Factory in Fabric**
   - Go to your Microsoft Fabric workspace
   - Click "New" → "Data Factory"
   - Name it: "RetailDataPipeline"

2. **Create New Pipeline**
   - Click "Create" → "Data pipeline"
   - Name: "SalesLT_to_Bronze_Pipeline"

### **Step 2: Configure Source Connection (Gaiye-SQL-DB)**

1. **Add Copy Data Activity**
   - In pipeline canvas, drag "Copy data" activity
   - Name it: "Copy_SalesLT_Tables"

2. **Configure Source Dataset**
   - Click "Source" tab
   - Click "New" to create source dataset
   - Select "Azure SQL Database"
   - **Connection Details:**
     ```
     Server name: Gaiye-SQL-DB.sql.fabric.microsoft.com
     Database name: Gaiye-SQL-DB
     Authentication: Azure Active Directory Integrated
     ```
   - Test connection to verify access

3. **Configure Source Query**
   ```sql
   -- Option 1: Copy all SalesLT tables (recommended)
   SELECT TABLE_NAME 
   FROM INFORMATION_SCHEMA.TABLES 
   WHERE TABLE_SCHEMA = 'SalesLT' 
   AND TABLE_TYPE = 'BASE TABLE'
   
   -- Option 2: Specific table query
   SELECT * FROM SalesLT.Customer
   ```

### **Step 3: Configure Destination (Bronze Layer)**

1. **Configure Sink Dataset**
   - Click "Destination" tab
   - Click "New" to create destination dataset
   - Select "Azure Data Lake Storage Gen2" or "Lakehouse"
   - **Connection Details:**
     ```
     Storage account: Your lakehouse storage
     Container: Files
     Directory: bronze/saleslt/
     File format: Parquet (recommended)
     ```

2. **Set File Organization**
   ```
   bronze/
   ├── saleslt/
   │   ├── customer/
   │   │   └── customer.parquet
   │   ├── product/
   │   │   └── product.parquet
   │   ├── salesorderheader/
   │   │   └── salesorderheader.parquet
   │   └── salesorderdetail/
   │       └── salesorderdetail.parquet
   ```

### **Step 4: Create Data Flow for Each Table**

#### **Method A: Individual Table Data Flows (Recommended)**

1. **Customer Table Data Flow**
   ```json
   {
     "name": "Customer_SalesLT_to_Bronze",
     "source": {
       "dataset": "SalesLT_Customer",
       "query": "SELECT *, GETDATE() as _extraction_timestamp, 'SalesLT.Customer' as _source_table FROM SalesLT.Customer"
     },
     "transformations": [
       {
         "type": "addColumns",
         "columns": {
           "_bronze_ingestion_timestamp": "currentTimestamp()",
           "_data_source": "'Gaiye-SQL-DB'",
           "_pipeline_run_id": "pipeline().RunId"
         }
       }
     ],
     "sink": {
       "dataset": "Bronze_Customer",
       "path": "Files/bronze/saleslt/customer/",
       "format": "parquet"
     }
   }
   ```

2. **Product Table Data Flow**
   ```json
   {
     "name": "Product_SalesLT_to_Bronze",
     "source": {
       "dataset": "SalesLT_Product",
       "query": "SELECT *, GETDATE() as _extraction_timestamp, 'SalesLT.Product' as _source_table FROM SalesLT.Product"
     },
     "transformations": [
       {
         "type": "addColumns",
         "columns": {
           "_bronze_ingestion_timestamp": "currentTimestamp()",
           "_data_source": "'Gaiye-SQL-DB'",
           "_pipeline_run_id": "pipeline().RunId"
         }
       }
     ],
     "sink": {
       "dataset": "Bronze_Product",
       "path": "Files/bronze/saleslt/product/",
       "format": "parquet"
     }
   }
   ```

#### **Method B: Dynamic Data Flow (Advanced)**

1. **Create Parameter-Driven Pipeline**
   ```json
   {
     "pipeline": {
       "parameters": {
         "tableList": [
           "Customer",
           "Product", 
           "SalesOrderHeader",
           "SalesOrderDetail",
           "Address",
           "ProductCategory"
         ]
       },
       "activities": [
         {
           "name": "ForEach_Table",
           "type": "ForEach",
           "items": "@pipeline().parameters.tableList",
           "activities": [
             {
               "name": "Copy_SalesLT_Table",
               "type": "Copy",
               "source": {
                 "query": "SELECT *, GETDATE() as _extraction_timestamp, 'SalesLT.@{item()}' as _source_table FROM SalesLT.@{item()}"
               },
               "sink": {
                 "path": "Files/bronze/saleslt/@{toLower(item())}/",
                 "fileName": "@{toLower(item())}.parquet"
               }
             }
           ]
         }
       ]
     }
   }
   ```

### **Step 5: Add Data Quality and Monitoring**

1. **Data Validation Transformations**
   ```javascript
   // Add data quality checks in Data Flow
   
   // Check for null primary keys
   filter(not(isNull(CustomerID)))
   
   // Add data quality score
   derive(
     _data_quality_score = case(
       isNull(EmailAddress), 0,
       isNull(FirstName), 25,
       isNull(LastName), 50,
       true(), 100
     ),
     _record_status = case(
       _data_quality_score >= 75, 'GOOD',
       _data_quality_score >= 50, 'FAIR',
       true(), 'POOR'
     )
   )
   ```

2. **Error Handling Configuration**
   ```json
   {
     "errorHandling": {
       "skipErrorFiles": false,
       "skipErrorRows": true,
       "maxErrorCount": 100,
       "errorOutputPath": "Files/bronze/saleslt/_errors/"
     },
     "monitoring": {
       "logLevel": "Information",
       "enableDataFlowDebug": true,
       "alertOnFailure": true
     }
   }
   ```

### **Step 6: Configure Pipeline Triggers**

1. **Manual Trigger** (for testing)
   ```json
   {
     "trigger": {
       "name": "ManualTrigger",
       "type": "Manual"
     }
   }
   ```

2. **Scheduled Trigger** (for ongoing updates)
   ```json
   {
     "trigger": {
       "name": "DailyRefresh",
       "type": "Schedule",
       "schedule": {
         "frequency": "Day",
         "interval": 1,
         "startTime": "2025-01-01T02:00:00Z",
         "timeZone": "UTC"
       }
     }
   }
   ```

3. **Event-Based Trigger** (for real-time updates)
   ```json
   {
     "trigger": {
       "name": "DataChangeTrigger",
       "type": "BlobEventsTrigger",
       "scope": "/subscriptions/{subscription}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}",
       "events": ["Microsoft.Storage.BlobCreated"]
     }
   }
   ```

---

## **Implementation Checklist**

### **Pre-Implementation**
- [ ] ✅ Verify access to Gaiye-SQL-DB
- [ ] ✅ Confirm read permissions on SalesLT schema
- [ ] ✅ Ensure lakehouse write permissions
- [ ] ✅ Test connectivity between source and destination

### **Pipeline Configuration**
- [ ] 📊 Create Data Factory in Fabric workspace
- [ ] 🔗 Configure source connection to Gaiye-SQL-DB
- [ ] 📁 Set up bronze layer destination paths
- [ ] 🔄 Create data flows for each table
- [ ] ✨ Add data quality transformations
- [ ] 📝 Configure error handling and logging

### **Testing & Validation**
- [ ] 🧪 Test pipeline with single table first
- [ ] 📈 Validate data in bronze layer
- [ ] 🔍 Check error logs and data quality metrics
- [ ] 📊 Verify all SalesLT tables copied successfully
- [ ] 🔄 Test incremental data loading

### **Production Deployment**
- [ ] ⏰ Set up appropriate triggers
- [ ] 📧 Configure monitoring and alerts
- [ ] 📋 Document pipeline for team
- [ ] 🚀 Schedule regular data refreshes

---

## **Sample Data Flow JSON Template**

```json
{
  "name": "SalesLT_to_Bronze_Complete",
  "properties": {
    "activities": [
      {
        "name": "Copy_All_SalesLT_Tables",
        "type": "ForEach",
        "dependsOn": [],
        "typeProperties": {
          "items": {
            "value": "@variables('tableList')",
            "type": "Expression"
          },
          "isSequential": false,
          "batchCount": 3,
          "activities": [
            {
              "name": "Copy_Table",
              "type": "Copy",
              "policy": {
                "timeout": "7.00:00:00",
                "retry": 3,
                "retryIntervalInSeconds": 30
              },
              "typeProperties": {
                "source": {
                  "type": "AzureSqlSource",
                  "sqlReaderQuery": {
                    "value": "SELECT *, GETDATE() as _extraction_timestamp, 'SalesLT.@{item()}' as _source_table, '@{pipeline().RunId}' as _pipeline_run_id FROM SalesLT.@{item()}",
                    "type": "Expression"
                  },
                  "queryTimeout": "02:00:00"
                },
                "sink": {
                  "type": "ParquetSink",
                  "storeSettings": {
                    "type": "AzureBlobFSWriteSettings",
                    "copyBehavior": "FlattenHierarchy"
                  }
                },
                "enableStaging": false,
                "translator": {
                  "type": "TabularTranslator",
                  "typeConversion": true,
                  "typeConversionSettings": {
                    "allowDataTruncation": true,
                    "treatBooleanAsNumber": false
                  }
                }
              },
              "inputs": [
                {
                  "referenceName": "SalesLT_Source_Dataset",
                  "type": "DatasetReference"
                }
              ],
              "outputs": [
                {
                  "referenceName": "Bronze_Parquet_Dataset",
                  "type": "DatasetReference",
                  "parameters": {
                    "tableName": "@item()",
                    "filePath": "Files/bronze/saleslt/@{toLower(item())}/"
                  }
                }
              ]
            }
          ]
        }
      }
    ],
    "variables": {
      "tableList": {
        "type": "Array",
        "defaultValue": [
          "Customer",
          "Product",
          "SalesOrderHeader", 
          "SalesOrderDetail",
          "Address",
          "ProductCategory",
          "ProductModel",
          "ProductDescription"
        ]
      }
    }
  }
}
```

---

## **Monitoring and Troubleshooting**

### **Pipeline Monitoring**
1. **Real-time Monitoring**
   - Go to Data Factory → Monitor
   - View pipeline runs and activity details
   - Check data movement metrics

2. **Logging Configuration**
   ```json
   {
     "logging": {
       "enableCopyActivityLog": true,
       "copyActivityLogSettings": {
         "logLevel": "Info",
         "enableReliableLogging": true
       }
     }
   }
   ```

### **Common Issues and Solutions**

| **Issue** | **Cause** | **Solution** |
|-----------|-----------|--------------|
| Connection timeout | Network/auth issues | Check firewall, verify credentials |
| Permission denied | Insufficient RBAC | Grant SQL DB reader + Lakehouse contributor |
| Schema not found | Wrong database/schema | Verify Gaiye-SQL-DB and SalesLT schema |
| File write errors | Lakehouse permissions | Check storage account access |
| Data type errors | SQL to Parquet conversion | Add explicit type mappings |

### **Performance Optimization**
```json
{
  "performance": {
    "enableStaging": true,
    "stagingSettings": {
      "linkedServiceName": "BlobStagingLinkedService",
      "path": "staging/saleslt/"
    },
    "parallelCopies": 4,
    "dataIntegrationUnits": 8,
    "enableSkipIncompatibleRow": true
  }
}
```

---

## **Next Steps After Bronze Layer Setup**

1. **Silver Layer Pipeline**
   - Create data flows for data cleaning
   - Add business rules and validations
   - Implement data quality scoring

2. **Gold Layer Pipeline**
   - Build aggregated analytics tables
   - Create customer and product insights
   - Implement retail KPI calculations

3. **Monitoring Dashboard**
   - Set up Power BI dashboard
   - Create data quality reports
   - Monitor pipeline performance

4. **Automation**
   - Set up CI/CD for pipeline deployment
   - Create automated testing
   - Implement data lineage tracking

---

## **Benefits of This Approach**

### **🚀 Enterprise Ready**
- Scalable to handle millions of records
- Built-in retry logic and error handling
- Professional monitoring and alerting

### **🔐 Security First**
- Integrated authentication with Fabric
- Encrypted data in transit and at rest
- Role-based access control

### **📊 Data Quality**
- Built-in data validation
- Error tracking and reporting
- Data lineage and impact analysis

### **⚡ Performance**
- Parallel processing capabilities
- Optimized data movement
- Incremental loading support

---

This Data Factory approach will provide a much more robust, scalable, and maintainable solution compared to notebook-based data movement. Would you like me to help you implement any specific part of this pipeline?
