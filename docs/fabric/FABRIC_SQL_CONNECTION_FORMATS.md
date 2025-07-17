# Microsoft Fabric Data Factory - SQL Server Connection Guide

## 🔗 Connection Formats for Gaiye-SQL-DB

### **Primary Connection Format (Recommended)**
```
Server: Gaiye-SQL-DB.sql.fabric.microsoft.com
Port: 1433 (optional)
Database: Gaiye-SQL-DB
Authentication: Azure Active Directory Integrated
```

### **Alternative Connection Formats**

#### **Format 1: With Explicit Port**
```
Server: Gaiye-SQL-DB.sql.fabric.microsoft.com:1433
Database: Gaiye-SQL-DB
```

#### **Format 2: TCP Protocol Explicit**
```
Server: tcp:Gaiye-SQL-DB.sql.fabric.microsoft.com,1433
Database: Gaiye-SQL-DB
```

#### **Format 3: Datawarehouse Endpoint**
```
Server: Gaiye-SQL-DB.datawarehouse.fabric.microsoft.com
Port: 1433
Database: Gaiye-SQL-DB
```

## 📋 Data Factory Configuration Steps

### **Step 1: Create Linked Service**

1. **Navigate to Data Factory**
   - Go to your Fabric workspace
   - Open Data Factory
   - Click "Manage" → "Linked Services"

2. **Create New Linked Service**
   - Click "New"
   - Select "Azure SQL Database"
   - Name: `GaiyeSQLDB_LinkedService`

3. **Connection Configuration**
   ```json
   {
     "name": "GaiyeSQLDB_LinkedService",
     "properties": {
       "type": "AzureSqlDatabase",
       "typeProperties": {
         "server": "Gaiye-SQL-DB.sql.fabric.microsoft.com",
         "database": "Gaiye-SQL-DB",
         "authenticationType": "SystemAssignedManagedIdentity",
         "encrypt": "mandatory",
         "trustServerCertificate": false,
         "connectionTimeout": 30,
         "commandTimeout": 120
       }
     }
   }
   ```

### **Step 2: Create Source Dataset**

1. **Create Dataset**
   - Click "Author" → "Datasets"
   - Click "New Dataset"
   - Select "Azure SQL Database"

2. **Dataset Configuration**
   ```json
   {
     "name": "SalesLT_Source_Dataset",
     "properties": {
       "linkedServiceName": "GaiyeSQLDB_LinkedService",
       "type": "AzureSqlTable",
       "typeProperties": {
         "schema": "SalesLT",
         "table": "Customer"
       }
     }
   }
   ```

### **Step 3: Create Parameterized Dataset**

For dynamic table loading:
```json
{
  "name": "SalesLT_Dynamic_Dataset", 
  "properties": {
    "linkedServiceName": "GaiyeSQLDB_LinkedService",
    "parameters": {
      "TableName": {
        "type": "String"
      }
    },
    "type": "AzureSqlTable",
    "typeProperties": {
      "schema": "SalesLT",
      "table": {
        "value": "@dataset().TableName",
        "type": "Expression"
      }
    }
  }
}
```

## 🚀 Pipeline Implementation

### **Complete Pipeline JSON**

```json
{
  "name": "SalesLT_to_Bronze_Pipeline",
  "properties": {
    "activities": [
      {
        "name": "Get_SalesLT_Tables",
        "type": "Lookup",
        "typeProperties": {
          "source": {
            "type": "AzureSqlSource",
            "sqlReaderQuery": "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'SalesLT' AND TABLE_TYPE = 'BASE TABLE'"
          },
          "dataset": {
            "referenceName": "SalesLT_Source_Dataset",
            "type": "DatasetReference"
          },
          "firstRowOnly": false
        }
      },
      {
        "name": "ForEach_Table",
        "type": "ForEach",
        "dependsOn": [
          {
            "activity": "Get_SalesLT_Tables",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "items": {
            "value": "@activity('Get_SalesLT_Tables').output.value",
            "type": "Expression"
          },
          "isSequential": false,
          "batchCount": 3,
          "activities": [
            {
              "name": "Copy_SalesLT_Table",
              "type": "Copy",
              "typeProperties": {
                "source": {
                  "type": "AzureSqlSource",
                  "sqlReaderQuery": {
                    "value": "SELECT *, GETDATE() as _extraction_timestamp, 'SalesLT.@{item().TABLE_NAME}' as _source_table, '@{pipeline().RunId}' as _pipeline_run_id FROM SalesLT.@{item().TABLE_NAME}",
                    "type": "Expression"
                  }
                },
                "sink": {
                  "type": "ParquetSink",
                  "storeSettings": {
                    "type": "AzureBlobFSWriteSettings"
                  }
                },
                "enableStaging": false,
                "parallelCopies": 4
              },
              "inputs": [
                {
                  "referenceName": "SalesLT_Dynamic_Dataset",
                  "type": "DatasetReference",
                  "parameters": {
                    "TableName": "@item().TABLE_NAME"
                  }
                }
              ],
              "outputs": [
                {
                  "referenceName": "Bronze_Parquet_Dataset",
                  "type": "DatasetReference",
                  "parameters": {
                    "FolderPath": "Files/bronze/saleslt/@{toLower(item().TABLE_NAME)}",
                    "FileName": "@{toLower(item().TABLE_NAME)}.parquet"
                  }
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

## 🔧 Troubleshooting Connection Issues

### **Common Issues and Solutions**

| **Issue** | **Solution** |
|-----------|--------------|
| **"Login timeout expired"** | Add `,1433` to server name |
| **"Cannot open server"** | Try `.datawarehouse.fabric.microsoft.com` endpoint |
| **"Login failed"** | Check Azure AD permissions |
| **"Server not found"** | Verify spelling: `Gaiye-SQL-DB` |
| **"SSL connection error"** | Add `Encrypt=yes;TrustServerCertificate=no` |

### **Connection String Variations to Try**

#### **Option 1: Standard Fabric SQL**
```
Server=Gaiye-SQL-DB.sql.fabric.microsoft.com;Database=Gaiye-SQL-DB;Authentication=Active Directory Integrated;Encrypt=yes;
```

#### **Option 2: With Port**
```
Server=Gaiye-SQL-DB.sql.fabric.microsoft.com,1433;Database=Gaiye-SQL-DB;Authentication=Active Directory Integrated;Encrypt=yes;
```

#### **Option 3: Datawarehouse Endpoint**
```
Server=Gaiye-SQL-DB.datawarehouse.fabric.microsoft.com;Database=Gaiye-SQL-DB;Authentication=Active Directory Integrated;Encrypt=yes;
```

#### **Option 4: TCP Explicit**
```
Server=tcp:Gaiye-SQL-DB.sql.fabric.microsoft.com,1433;Database=Gaiye-SQL-DB;Authentication=Active Directory Integrated;Encrypt=yes;Connection Timeout=30;
```

## 📊 Testing the Connection

### **1. Test in Data Factory**
```json
{
  "testConnection": {
    "server": "Gaiye-SQL-DB.sql.fabric.microsoft.com",
    "database": "Gaiye-SQL-DB",
    "authenticationType": "ActiveDirectoryIntegrated"
  }
}
```

### **2. Test Query**
```sql
SELECT 
    COUNT(*) as table_count,
    'SalesLT' as schema_name
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'SalesLT'
```

### **3. Sample Data Query**
```sql
SELECT TOP 5 
    CustomerID,
    FirstName,
    LastName,
    EmailAddress,
    GETDATE() as extraction_time
FROM SalesLT.Customer
```

## 🎯 Expected Tables in SalesLT Schema

When connection is successful, you should see these tables:

- **SalesLT.Customer** - Customer master data
- **SalesLT.Product** - Product catalog
- **SalesLT.SalesOrderHeader** - Order headers
- **SalesLT.SalesOrderDetail** - Order line items
- **SalesLT.Address** - Address information
- **SalesLT.ProductCategory** - Product categories
- **SalesLT.ProductModel** - Product models
- **SalesLT.ProductDescription** - Product descriptions

## 🚀 Next Steps After Connection

1. **Test Single Table Copy**
   - Start with `SalesLT.Customer` table
   - Verify data appears in bronze layer

2. **Implement Full Pipeline**
   - Use the ForEach loop for all tables
   - Add error handling and monitoring

3. **Validate Bronze Layer**
   - Check file structure: `Files/bronze/saleslt/customer/customer.parquet`
   - Verify metadata columns are added

4. **Connect to Silver/Gold Pipeline**
   - Use the updated `fabric_retail_pipeline.py` 
   - Set `data_source_type='fabric_bronze'`

---

**💡 Pro Tip:** Always test the connection with a simple table first (like Customer) before running the full pipeline. This helps identify connection issues quickly.
