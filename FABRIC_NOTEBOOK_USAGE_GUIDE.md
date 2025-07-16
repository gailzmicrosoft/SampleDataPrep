# Microsoft Fabric Notebook Usage Guide: Export SalesLT to Bronze Layer

## Overview
This guide provides step-by-step instructions for using the `Export_SalesLT_to_Bronze.ipynb` notebook in Microsoft Fabric to export all SalesLT schema tables from your Gaiye-SQL-DB to the retail data model bronze layer.

## Prerequisites

### 1. Fabric Workspace Setup
- Access to Microsoft Fabric workspace
- Gaiye-SQL-DB Fabric SQL database available in your workspace
- Retail data model lakehouse created and accessible
- Appropriate permissions for SQL database read and lakehouse write operations

### 2. Required Permissions
- **SQL Database**: Read access to SalesLT schema tables
- **Lakehouse**: Write access to Files/bronze directory
- **Workspace**: Contributor or Admin role in the Fabric workspace

## Step-by-Step Implementation Guide

### Step 1: Upload the Notebook to Fabric
1. **Navigate to your Fabric workspace**
   - Go to https://fabric.microsoft.com
   - Select your workspace where Gaiye-SQL-DB is located

2. **Import the notebook**
   - Click "New" → "Import notebook"
   - Upload the `Export_SalesLT_to_Bronze.ipynb` file
   - Name it "Export SalesLT to Bronze Layer"

### Step 2: Configure Lakehouse Connection
1. **Attach the lakehouse**
   - Open the uploaded notebook
   - In the notebook toolbar, click "Add lakehouse"
   - Select "Existing lakehouse"
   - Choose your retail data model lakehouse
   - Click "Add"

2. **Verify lakehouse attachment**
   - You should see the lakehouse name in the left panel
   - Ensure you can see the "Files" folder structure

### Step 3: Verify Database Connection Settings
1. **Check connection string (Cell 3)**
   - The notebook uses: `Gaiye-SQL-DB.sql.fabric.microsoft.com`
   - If your database has a different endpoint, update the connection string
   - The notebook uses integrated authentication (recommended for Fabric)

2. **Test connection**
   - Run Cell 3 to test the database connection
   - Look for "✅ Database connection successful" message
   - If connection fails, verify database name and permissions

### Step 4: Execute the Notebook

#### Run Each Cell Sequentially:

**Cell 1 (Markdown)**: Introduction and prerequisites
- Read the overview and ensure prerequisites are met

**Cell 2 (Python)**: Import libraries
- Run to import required Python packages
- Verify "✅ Libraries imported successfully" message

**Cell 3 (Python)**: Database connection test
- Tests connection to Gaiye-SQL-DB
- Should show "✅ Database connection successful"

**Cell 4 (Python)**: Discover SalesLT tables
- Automatically finds all tables in SalesLT schema
- Lists discovered tables (typically includes Customer, Product, Order, etc.)

**Cell 5 (Python)**: Define export function
- Sets up the table export logic
- Adds metadata tracking for each exported table

**Cell 6 (Python)**: Execute bulk export
- Exports all discovered tables to bronze layer
- Shows progress for each table
- Displays success/failure status with row counts

**Cell 7 (Python)**: Generate summary report
- Creates detailed export summary
- Shows total rows and file sizes
- Saves summary JSON file

**Cell 8 (Python)**: Validation
- Verifies files exist in bronze layer
- Lists all exported files and directories

**Cell 9 (Markdown)**: Next steps and troubleshooting
- Read for post-export recommendations

### Step 5: Verify Export Results

#### Check Bronze Layer Structure:
```
Files/
└── bronze/
    ├── address/
    │   └── address.parquet
    ├── customer/
    │   └── customer.parquet
    ├── customeraddress/
    │   └── customeraddress.parquet
    ├── product/
    │   └── product.parquet
    ├── productcategory/
    │   └── productcategory.parquet
    ├── productdescription/
    │   └── productdescription.parquet
    ├── productmodel/
    │   └── productmodel.parquet
    ├── productmodelproductdescription/
    │   └── productmodelproductdescription.parquet
    ├── salesorderdetail/
    │   └── salesorderdetail.parquet
    ├── salesorderheader/
    │   └── salesorderheader.parquet
    └── _export_summary.json
```

#### Verify Data Quality:
1. **Check row counts**: Compare with source tables
2. **Validate file sizes**: Ensure reasonable file sizes
3. **Review metadata**: Each file includes source tracking
4. **Examine summary**: Review the JSON summary report

## Expected Export Results

### Typical SalesLT Tables:
- **Address**: Customer and business addresses
- **Customer**: Customer master data
- **CustomerAddress**: Customer-address relationships
- **Product**: Product catalog information
- **ProductCategory**: Product categorization
- **ProductDescription**: Product descriptions and details
- **ProductModel**: Product model information
- **ProductModelProductDescription**: Model-description relationships
- **SalesOrderDetail**: Order line items
- **SalesOrderHeader**: Order headers and customer information

### Metadata Added to Each File:
- `_source_table`: Original table name (e.g., "SalesLT.Customer")
- `_extraction_timestamp`: When the data was exported
- `_source_database`: Source database name ("Gaiye-SQL-DB")

## Troubleshooting Common Issues

### Connection Problems
**Error**: "Connection failed"
**Solutions**:
- Verify database name matches exactly: "Gaiye-SQL-DB"
- Check workspace permissions for SQL database access
- Ensure you're in the correct Fabric workspace
- Try refreshing the notebook kernel

### Permission Issues
**Error**: "Access denied to schema SalesLT"
**Solutions**:
- Contact workspace admin for SalesLT schema read permissions
- Verify you have SQL database reader role
- Check if database exists and is accessible in current workspace

### Lakehouse Issues
**Error**: "Cannot write to Files/bronze"
**Solutions**:
- Ensure lakehouse is properly attached to notebook
- Verify write permissions to the lakehouse
- Check if Files folder exists (create if missing)
- Try running with a different lakehouse

### Large Table Handling
**Error**: "Memory error" or "Timeout"
**Solutions**:
- For tables with >1M rows, consider chunked processing
- Use `LIMIT` clauses for initial testing
- Increase notebook compute resources if available
- Process largest tables separately

### Data Type Issues
**Error**: "Data type conversion error"
**Solutions**:
- Review SQL Server data types in source tables
- Add explicit type casting in SQL queries if needed
- Check for special characters or encoding issues
- Use pandas data type specifications for problematic columns

## Post-Export Next Steps

### 1. Data Validation
- **Row count verification**: Compare source vs. exported counts
- **Data sampling**: Spot-check data quality and completeness
- **Schema validation**: Verify all expected columns are present
- **Relationship integrity**: Check foreign key relationships

### 2. Silver Layer Development
- **Data cleansing**: Remove duplicates, handle nulls
- **Standardization**: Apply consistent formatting and naming
- **Type conversions**: Ensure proper data types for analytics
- **Business rules**: Apply domain-specific transformations

### 3. Gold Layer Implementation
- **Dimensional modeling**: Create fact and dimension tables
- **Aggregations**: Build summary tables for reporting
- **Business metrics**: Calculate KPIs and derived measures
- **Performance optimization**: Implement partitioning and indexing

### 4. Pipeline Automation
- **Incremental loads**: Set up delta processing for ongoing updates
- **Scheduling**: Automate regular data refreshes
- **Monitoring**: Implement data quality and freshness checks
- **Error handling**: Create robust error recovery procedures

## Additional Resources

### Fabric Documentation
- [Microsoft Fabric Lakehouse](https://docs.microsoft.com/fabric/data-engineering/lakehouse-overview)
- [Fabric SQL Database](https://docs.microsoft.com/fabric/data-warehouse/sql-database)
- [Notebook Development](https://docs.microsoft.com/fabric/data-engineering/how-to-use-notebook)

### Retail Data Model Resources
- [Retail Industry Solutions](https://docs.microsoft.com/industry/retail/)
- [Common Data Model for Retail](https://github.com/microsoft/CDM/tree/master/schemaDocuments/core/industryCommon/Retail)
- [Medallion Architecture Best Practices](https://docs.microsoft.com/azure/databricks/lakehouse/medallion)

## Success Criteria

✅ **All SalesLT tables exported successfully**
✅ **Bronze layer properly organized with Parquet files**
✅ **Metadata tracking implemented**
✅ **Export summary report generated**
✅ **File validation completed**
✅ **Ready for silver layer development**

## Support and Escalation

If you encounter issues not covered in this guide:

1. **Check Fabric workspace health**: Verify all resources are running
2. **Review activity logs**: Check for system-level errors
3. **Test with smaller datasets**: Isolate problematic tables
4. **Contact workspace admin**: For permission-related issues
5. **Microsoft Support**: For platform-specific problems

---

*This guide provides comprehensive instructions for using the Export_SalesLT_to_Bronze.ipynb notebook in Microsoft Fabric. Follow the steps sequentially and refer to the troubleshooting section for common issues.*
