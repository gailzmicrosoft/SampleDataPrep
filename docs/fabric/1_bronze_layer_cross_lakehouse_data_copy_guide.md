# Bronze Layer Cross-Lakehouse Data Copy - A Working Solution

## The Challenge We Solved

**Problem**: Copying data between lakehouses in Microsoft Fabric can be tricky, especially when you need a reliable, simple approach that works consistently without complex dependencies.

**Common Issues**:
- `dbutils` not available in Fabric PySpark notebooks
- Cross-lakehouse data access confusion
- Complex setup requirements that break easily
- No clear guidance on dual storage (Files + Tables)
- PySpark notebooks can't directly see SQL Server data sources

**Our Solution**: A simplified, pure SQL approach that reliably copies SalesLT tables from one lakehouse to another with dual storage and metadata enrichment.

## What We Built

📁 **Location**: `src/notebooks/SalesLT_to_Retail_Data_Bronze.ipynb`

A streamlined 5-step notebook that:
1. **Environment Setup** - Configuration and library imports
2. **Discover Available Tables** - Find source tables with troubleshooting
3. **Test Bronze Layer Access** - Verify write permissions
4. **Process SalesLT Tables to Bronze** - Core dual storage processing
5. **Validate Bronze Layer Data** - Quality assurance and reporting

## Key Architecture Decisions

### Cross-Lakehouse Setup
- **Original Source**: SalesLT sample data in Fabric SQL Server
- **Visibility Challenge**: PySpark notebooks can't directly access SQL Server data sources
- **Workaround**: Created intermediate lakehouse (`Gaiye_Test_Lakehouse`) with shortcuts to SQL Server tables
- **Execution Context**: Run notebook in the target bronze lakehouse
- **Source Access**: Use qualified database names (`SOURCE_DATABASE.tablename`) to access shortcut data
- **Data Flow**: SQL Server → Intermediate Lakehouse (shortcuts) → Bronze Lakehouse (Files + Tables)

### Dual Storage Strategy
- **Files**: Parquet files in `Files/SalesLT/` for file-based processing
- **Tables**: Managed lakehouse tables with `bronze_` prefix for SQL analytics
- **Metadata**: Rich tracking columns added to every record

### Simplified Approach
- **No dbutils**: Pure PySpark SQL approach that works reliably
- **Error Handling**: Graceful failure handling and clear troubleshooting
- **Flexible Execution**: Multiple workflow options for different use cases

## Real-World Architecture

### The Data Visibility Challenge
Our original source was **SalesLT sample data in a Fabric SQL Server**, but we discovered that **PySpark notebooks cannot directly see SQL Server data sources**. This is a common frustration that many Fabric users encounter.

### The Shortcut Workaround
**Solution**: Create an intermediate lakehouse as a bridge:

```
SQL Server (SalesLT data) 
    ↓ (shortcuts)
Intermediate Lakehouse (Gaiye_Test_Lakehouse)
    ↓ (qualified queries)
Bronze Lakehouse (dual storage)
```

**Steps we took**:
1. Created a new lakehouse (`Gaiye_Test_Lakehouse`) 
2. Added shortcuts from this lakehouse to the SQL Server SalesLT tables
3. Set this intermediate lakehouse as our `SOURCE_DATABASE`
4. Now the bronze notebook can see and access the data via qualified database names

This pattern works reliably and gives you the visibility you need for cross-source data movement.

## Getting Started (The Easy Way)

### Prerequisites
1. Microsoft Fabric workspace with PySpark runtime
2. Source data in SQL Server (SalesLT sample data in our case)
3. Intermediate lakehouse with shortcuts to SQL Server tables (workaround for visibility)
4. Target bronze lakehouse with write permissions
5. Shortcut configured from bronze to intermediate lakehouse

### First Time Setup
1. **Create intermediate lakehouse** (if your source is SQL Server)
   - Create new lakehouse (e.g., `YourSource_Lakehouse`)
   - Add shortcuts to your SQL Server tables
2. **Configure the notebook** in your bronze lakehouse
3. Update the configuration in Step 1:
   ```python
   SOURCE_DATABASE = "YourSource_Lakehouse"  # Your intermediate lakehouse name
   EXPECTED_TABLES = ['your', 'table', 'names']  # Your table names
   ```
4. Run all steps (1-5) for complete setup and validation

### Regular Usage (The Fast Way)
Once working, you can run just:
- **Steps 1 + 4** for fastest data refresh (our recommended approach)
- **Steps 1 + 4 + 5** if you want validation included

## Why This Works

### Technical Advantages
- **Qualified Database Access**: `SELECT * FROM SourceDB.tablename` bypasses many permission issues
- **Dual Storage**: Files for ETL flexibility, Tables for SQL analytics
- **Metadata Enrichment**: Load tracking, timestamps, and lineage built-in
- **Error Recovery**: Clear troubleshooting guidance when things go wrong

### Practical Benefits
- **Reliable**: Works consistently across different Fabric environments
- **Simple**: No complex dependencies or setup requirements
- **Fast**: Optimized workflow options for different scenarios
- **Maintainable**: Clear code structure that team members can understand

## Real-World Usage Patterns

### Development Workflow
```
First Run: Steps 1-5 (validate everything works)
Iterations: Steps 1,4 (fast development cycles)
Production: Steps 1,4 (scheduled refreshes)
```

### Team Adoption
- **New Team Members**: Run all steps first time, then use Steps 1+4
- **Scheduled Jobs**: Use Steps 1+4 for fastest execution
- **Debugging**: Run Step 5 when you need detailed validation

## Common Issues & Solutions

### "No tables found" Error
- Check shortcut configuration in bronze lakehouse
- Verify intermediate lakehouse contains expected shortcuts to source data
- Refresh lakehouse view in Fabric UI
- Ensure SOURCE_DATABASE name matches your intermediate lakehouse name

### SQL Server Visibility Issues
- Create intermediate lakehouse with shortcuts to SQL Server tables
- PySpark notebooks cannot directly access SQL Server - shortcuts are the workaround
- Verify shortcuts are properly configured and showing data in lakehouse explorer

### Permission Errors
- Ensure you have read access to source lakehouse
- Verify write permissions in bronze lakehouse
- Check workspace-level permissions

### Performance Considerations
- Large tables: Consider partitioning strategy
- Frequent runs: Use Steps 1+4 workflow
- Monitoring: Step 5 provides detailed metrics

## Lessons Learned

### What We Tried First (Didn't Work)
- Direct access to SQL Server from PySpark notebooks (not supported)
- Complex `dbutils` approaches (not available in Fabric)
- Overly sophisticated discovery mechanisms
- Too many validation steps (slowed down regular use)

### What Actually Works
- Intermediate lakehouse with shortcuts to SQL Server (solves visibility)
- Simple qualified database names for cross-lakehouse access
- Pure PySpark SQL approach
- Flexible workflow options
- Clear error messaging and troubleshooting

### Best Practices 
- Always run in the target lakehouse context
- Use qualified database names for cross-lakehouse access
- Implement dual storage from the start
- Provide multiple workflow options for different use cases

## Next Steps

Once you have bronze layer working:
1. **Silver Layer**: Implement data transformations and quality rules
2. **Incremental Loading**: Add change detection and delta processing
3. **Gold Layer**: Create business-ready aggregations and marts
4. **Monitoring**: Add data quality monitoring and alerting

