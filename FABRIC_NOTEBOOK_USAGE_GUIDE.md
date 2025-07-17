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

### Step 3: Handle Authentication Challenges
⚠️ **Important**: Direct notebook authentication to Azure SQL has known limitations in Fabric

1. **Run Cell 3 (Authentication Test)**
   - The notebook will test multiple authentication methods
   - **If you have lakehouse shortcuts**: "✅ Found X existing SalesLT tables in lakehouse"
   - **If no shortcuts**: Expected result: "⚠️ NO AUTHENTICATION METHOD WORKED"
   - This is normal and expected based on community feedback

2. **Choose Your Solution Path** (see options below):
   - **Option A**: Create Lakehouse Shortcuts (Recommended - Easiest) ✅
   - **Option B**: Use Data Factory Pipeline (Most Robust)
   - **Option C**: Manual Workspace Identity Setup (Advanced)

**Note**: Lakehouse shortcuts import SQL tables without the schema prefix. So `SalesLT.Customer` becomes just `Customer` in the lakehouse.

### Step 4: Choose Your Authentication Solution

Based on your test results, choose one of these approaches:

#### 🎯 **OPTION A: Lakehouse Shortcuts (Recommended)**
**Why this works**: No authentication issues, data appears as native tables

**Steps**:
1. **Go to your lakehouse**
   - Navigate to your retail data model lakehouse
   - Click on the "Tables" section in the left panel

2. **Create shortcuts**
   - Click "New shortcut" 
   - Select "Azure SQL Database"
   - **Server**: `gaiye-sql-db.sql.fabric.microsoft.com`
   - **Database**: `Gaiye-SQL-DB`
   - **Authentication**: Use workspace identity (automatic)

3. **Select SalesLT tables**
   - Browse to schema: `SalesLT`
   - Select all tables (or specific ones you need)
   - Click "Create"

4. **Re-run the notebook**
   - The notebook will automatically detect the shortcuts
   - Cell 3 will show: "✅ Found X existing SalesLT tables in lakehouse"
   - **Important**: Shortcuts appear as `Customer`, `Product`, etc. (no `SalesLT.` prefix)
   - Continue with normal execution

#### 🏭 **OPTION B: Data Factory Pipeline**
**Why this works**: Your existing connections work perfectly in Data Factory

**Steps**:
1. **Create new Data Factory**
   - In your workspace, click "New" → "Data Factory"
   - Name it "SalesLT Export Pipeline"

2. **Use existing connection**
   - Create pipeline with connection: `gaiye-sql-db.sql.fabric.microsoft;SalesLT gazho`
   - This connection already works in Data Factory

3. **Create copy activities**
   - Add "Copy Data" activity for each SalesLT table
   - Source: SQL Server tables
   - Destination: Lakehouse `Files/bronze/saleslt/`
   - Format: Parquet

4. **Schedule and run**
   - Set up schedule for regular updates
   - Manual trigger for immediate execution

#### 🔧 **OPTION C: Manual Workspace Identity (Advanced)**
**Warning**: Requires Azure admin permissions, mixed success rate

**Steps**:
1. **Get workspace identity name**
   - In Fabric workspace settings, find the workspace identity
   - Copy the full identity name

2. **Azure Portal SQL Server setup**
   - Go to Azure Portal → SQL Servers → gaiye-sql-db
   - Navigate to "Security" → "Azure Active Directory"
   - Add workspace identity as SQL admin or db_datareader

3. **Test connection**
   - Re-run Cell 3 in the notebook
   - Look for successful workspace identity authentication

### Step 5: Execute the Notebook (After Authentication Setup)

#### Run Each Cell Sequentially:

**Cell 1 (Markdown)**: Introduction and prerequisites
- Read the overview and ensure prerequisites are met

**Cell 2 (Python)**: Import libraries
- Run to import required Python packages
- Verify "✅ Libraries imported successfully" message

**Cell 3 (Python)**: Authentication testing
- Tests multiple authentication methods
- If shortcuts created: "✅ Found existing SalesLT-related tables"
- If no solution: Follow authentication setup guidance

**Cell 4 (Python)**: Discover SalesLT tables
- Automatically finds all tables based on your chosen authentication method
- Lists discovered tables (Customer, Product, Orders, etc.)

**Cell 5 (Python)**: Define export function
- Sets up the table export logic with authentication awareness
- Adds metadata tracking for each exported table

**Cell 6 (Python)**: Execute bulk export
- Exports all discovered tables to bronze layer
- Shows progress for each table with authentication method used
- Displays success/failure status with row counts

**Cell 7 (Python)**: Troubleshooting and next steps
- Provides guidance based on authentication results
- Recommendations for production setup

**Cell 8 (Python)**: Validation
- Verifies files exist in bronze layer
- Lists all exported files and directories

### Step 6: Verify Export Results
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

## Authentication Issues (Known Limitations)

### Why Direct Notebook Authentication Fails
Based on Microsoft Fabric community feedback:
- **Workspace Identity vs User Token**: Fabric notebooks often get user tokens instead of workspace tokens
- **JDBC Connector Issues**: `com.microsoft.sqlserver.jdbc.spark` format has known limitations in Fabric
- **Token Scope Problems**: Azure SQL Database tokens may not work correctly from notebook context
- **Authentication Mode Conflicts**: ActiveDirectoryMSI may not be properly configured

### Community-Recommended Solutions (In Order of Preference)

1. **Lakehouse Shortcuts** ✅ Most Reliable
   - No authentication issues in notebooks
   - Data appears as native lakehouse tables
   - Automatic refresh capabilities
   - Easiest to set up and maintain

2. **Data Factory Pipelines** ✅ Most Robust
   - Your existing connections work perfectly
   - Better authentication handling
   - Full ETL/ELT capabilities
   - Production-ready scheduling

3. **Workspace Identity Setup** ⚠️ Advanced/Mixed Results
   - Requires Azure admin permissions
   - Community reports inconsistent success
   - Complex permission management

## Troubleshooting Common Issues

### Authentication Problems
**Error**: "⚠️ NO AUTHENTICATION METHOD WORKED"
**Solutions**:
- **Expected behavior** - This is a known limitation
- Choose lakehouse shortcuts (recommended)
- Use Data Factory instead of notebook
- Contact Azure admin for workspace identity setup

### Lakehouse Shortcuts Issues
**Error**: "Cannot create shortcut to SQL Server"
**Solutions**:
- Verify you have lakehouse contributor permissions
- Check if SQL Server allows external connections
- Ensure workspace identity has SQL Server access
- Try creating shortcut to individual tables instead of schema

### Data Factory Connection Issues
**Error**: "Connection test failed in Data Factory"
**Solutions**:
- Use the existing connection: `gaiye-sql-db.sql.fabric.microsoft;SalesLT gazho`
- Don't create new connections - reuse existing ones
- Verify the connection works in Data Factory first
- Test with a simple copy activity on one table

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
