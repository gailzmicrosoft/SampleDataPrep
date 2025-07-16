## Fabric Notebook: Export SalesLT Tables to Bronze Layer

### Step 1: Setup and Connection
1. Create new Fabric Notebook in your workspace
2. Attach the retail data model lakehouse to the notebook
3. Import required libraries (pandas, pyodbc/sqlalchemy)
4. Establish connection to Gaiye-SQL-DB using Fabric's built-in SQL connectivity

### Step 2: Discover All SalesLT Tables
1. Query INFORMATION_SCHEMA.TABLES to get all table names in SalesLT schema
2. Filter for TABLE_TYPE = 'BASE TABLE' to exclude views
3. Store table names in a list for processing

`SELECT TABLE_NAME` 
`FROM INFORMATION_SCHEMA.TABLES` 
`WHERE TABLE_SCHEMA = 'SalesLT'` 
`AND TABLE_TYPE = 'BASE TABLE'`



SELECT * FROM SalesLT.{table_name}



### Step 3: Dynamic Data Export Loop

1. For each discovered table name:
   - Build dynamic SQL query: SELECT * FROM SalesLT.{table_name}
   - Execute query and load into pandas DataFrame
   - Handle any data type conversions automatically
   - Save DataFrame as Parquet file in bronze layer
   - Use table name as file/folder name
   - Add extraction timestamp metadata

### Step 4: Error Handling and Logging
1. Wrap each table export in try/catch blocks
2. Log successful exports and any errors
3. Continue processing even if one table fails
4. Track row counts for validation

### Step 5: Validation and Summary
1. Verify each exported file exists in bronze layer
2. Check row counts match between source and destination
3. Generate summary report of all exported tables
4. Display total tables processed, successful exports, and any errors

### Step 6: Notebook Structure
- Cell 1: Import libraries and setup
- Cell 2: Database connection
- Cell 3: Table discovery query
- Cell 4: Export loop function
- Cell 5: Execute export for all tables
- Cell 6: Validation and summary report

This approach will automatically discover and export all SalesLT tables without requiring you to specify table names, saving everything to your retail data model bronze layer as Parquet files ready for further