# Complete Microsoft Fabric & VS Code Development Setup Guide

> **Created**: July 18, 2025  
> **Purpose**: Comprehensive guide for setting up Microsoft Fabric development environment in VS Code  
> **Status**: ✅ Tested and Working

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [VS Code Extensions Setup](#vs-code-extensions-setup)
3. [Python Environment Configuration](#python-environment-configuration)
4. [Project Structure](#project-structure)
5. [Environment Testing](#environment-testing)
6. [Notebook Setup](#notebook-setup)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows (PowerShell)
- **Python**: 3.11.9 or later
- **VS Code**: Latest version
- **Git**: For repository management

### Azure/Fabric Access
- Microsoft Fabric workspace access
- Azure subscription (if using Azure resources)
- Appropriate permissions for Fabric lakehouse operations

---

## 🧩 VS Code Extensions Setup

### Required Extensions
Install these extensions in VS Code:

```bash
# Core Extensions
- Python (ms-python.python)
- Jupyter (ms-toolsai.jupyter)
- Pylance (ms-python.vscode-pylance)

# Microsoft Fabric Extensions
- Microsoft Fabric (fabric.vscode-fabric)
- Azure Synapse (synapsevscode.synapse)
- Fabric Studio (gerhardbrueckl.fabricstudio)

# Optional but Recommended
- Azure Account (ms-vscode.azure-account)
- Azure Resources (ms-azuretools.vscode-azureresourcegroups)
- PowerShell (ms-vscode.powershell)
```

### Installation Commands
```bash
# Install via VS Code Command Palette (Ctrl+Shift+P)
> Extensions: Install Extension
# Search for each extension name and install
```

---

## 🐍 Python Environment Configuration

### 1. Create Virtual Environment
```powershell
# Navigate to project root
cd C:\Repos\Code\SampleDataPrep

# Create virtual environment in src folder (organized structure)
python -m venv src\.venv
```

### 2. Install Required Packages
```powershell
# Install all required packages
src\.venv\Scripts\pip.exe install azure-storage-file-datalake azure-identity pyspark pandas pyarrow delta-spark
```

### 3. Package Versions (Verified Working)
```
azure-storage-file-datalake==12.25.0
azure-identity==1.23.1
pyspark==3.5.4
pandas==2.3.1
pyarrow==18.1.0
delta-spark==3.2.1
```

### 4. Configure VS Code Python Interpreter
1. Open VS Code in project folder
2. Press `Ctrl+Shift+P`
3. Type "Python: Select Interpreter"
4. Choose: `src\.venv\Scripts\python.exe`

---

## 📁 Project Structure

```
C:\Repos\Code\SampleDataPrep\
├── src/
│   ├── .venv/                                # Python virtual environment
│   └── notebooks/
│       └── Bronze_to_Silver_Schema_Analysis.ipynb
├── infra/                                    # Bicep infrastructure files
│   ├── main.bicep
│   └── core/
│       ├── ai/
│       ├── database/
│       ├── host/
│       ├── monitor/
│       ├── security/
│       └── storage/
├── docs/                                     # Documentation
│   └── zta/                                  # Zero Trust Architecture docs
├── data/                                     # Sample data files
│   ├── customers.csv
│   ├── orders.csv
│   └── products.csv
├── scripts/                                  # Deployment scripts
├── test_fabric_connection.py                 # Environment test script
├── Export_SalesLT_to_Bronze.ipynb           # Working notebook
├── FABRIC_VSCODE_SETUP_GUIDE.md             # Original setup guide
├── COMPLETE_SETUP_GUIDE.md                  # This document
└── README.md
```

---

## 🧪 Environment Testing

### Test Script
Create and run `test_fabric_connection.py`:

```python
# Test script to verify all components work
import sys
import pandas as pd
from datetime import datetime

def test_environment():
    print("🔍 TESTING FABRIC DEVELOPMENT ENVIRONMENT")
    print("=" * 50)
    
    # Test 1: Python Environment
    print(f"✅ Python version: {sys.version}")
    print(f"✅ Virtual environment: {sys.prefix}")
    
    # Test 2: Core Libraries
    try:
        import azure.storage.filedatalake
        print("✅ Azure Storage File Data Lake imported successfully")
    except ImportError as e:
        print(f"❌ Azure Storage import failed: {e}")
    
    try:
        import azure.identity
        print("✅ Azure Identity imported successfully")
    except ImportError as e:
        print(f"❌ Azure Identity import failed: {e}")
    
    try:
        import pyspark
        print("✅ PySpark imported successfully")
    except ImportError as e:
        print(f"❌ PySpark import failed: {e}")
    
    # Test 3: Data Libraries
    print(f"✅ Pandas version: {pd.__version__}")
    
    try:
        import pyarrow
        print(f"✅ PyArrow version: {pyarrow.__version__}")
    except ImportError as e:
        print(f"❌ PyArrow import failed: {e}")
    
    try:
        import delta
        print("✅ Delta Spark imported successfully")
    except ImportError as e:
        print(f"❌ Delta Spark import failed: {e}")
    
    print("\n🎉 Environment test completed!")
    print(f"📅 Test timestamp: {datetime.now().isoformat()}")

if __name__ == "__main__":
    test_environment()
```

### Run Test
```powershell
src\.venv\Scripts\python.exe test_fabric_connection.py
```

**Expected Output:**
```
🔍 TESTING FABRIC DEVELOPMENT ENVIRONMENT
==================================================
✅ Python version: 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
✅ Virtual environment: C:\Repos\Code\SampleDataPrep\src\.venv
✅ Azure Storage File Data Lake imported successfully
✅ Azure Identity imported successfully
✅ PySpark imported successfully
✅ Pandas version: 2.3.1
✅ PyArrow version: 18.1.0
✅ Delta Spark imported successfully

🎉 Environment test completed!
📅 Test timestamp: 2025-07-18T[timestamp]
```

---

## 📓 Notebook Setup

### 1. Kernel Configuration
- **Issue**: Avoid "Fabric Data Engineering PySpark environment preparation failed"
- **Solution**: Use local Python interpreter instead of Fabric kernels

### 2. Working Notebook Template
Created `Export_SalesLT_to_Bronze.ipynb` with:

```python
# Cell 1: Environment Test
import sys
print(f"Python version: {sys.version}")
print(f"Virtual environment: {sys.prefix}")
print("✅ Kernel is working correctly!")

# Cell 2: Configuration
import pandas as pd
from datetime import datetime
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Configuration
BRONZE_DATABASE = "RDS_Fabric_Foundry_workspace_Gaiye_Retail_Solution_Test_IDM_LH_bronze"
SILVER_TARGET_PATH = "Files/Retail/"
SOURCE_SYSTEM = "SalesLT_to_Retail"
LOAD_TIMESTAMP = datetime.now().isoformat()
LOAD_DATE = datetime.now().strftime("%Y-%m-%d")

# Expected bronze tables (SalesLT)
BRONZE_TABLES = [
    'bronze_address', 'bronze_customer', 'bronze_customeraddress', 
    'bronze_product', 'bronze_productcategory', 'bronze_productdescription', 
    'bronze_productmodel', 'bronze_productmodelproductdescription', 
    'bronze_salesorderdetail', 'bronze_salesorderheader'
]

# Key silver target entities
SILVER_MAIN_ENTITIES = ['order', 'customer', 'brandProduct']

print("🔍 BRONZE TO SILVER SCHEMA ANALYSIS")
print("=" * 60)
print(f"✅ Libraries imported")
print(f"📅 Analysis timestamp: {LOAD_TIMESTAMP}")
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Kernel Hanging
**Problem**: "Fabric Data Engineering PySpark environment preparation failed"
**Solution**: 
- Use local Python interpreter: `src\.venv\Scripts\python.exe`
- Avoid Fabric-specific kernels in VS Code
- Start with simple test cell before running complex code

#### 2. Import Errors
**Problem**: Module not found errors
**Solution**:
```powershell
# Reinstall packages
src\.venv\Scripts\pip.exe install --upgrade [package-name]

# Verify installation
src\.venv\Scripts\pip.exe list
```

#### 3. VS Code Python Interpreter
**Problem**: Wrong Python interpreter selected
**Solution**:
1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose: `src\.venv\Scripts\python.exe`
3. Restart VS Code if needed

#### 4. Virtual Environment Issues
**Problem**: Environment not recognized
**Solution**:
```powershell
# Recreate environment
Remove-Item -Recurse -Force src\.venv
python -m venv src\.venv
src\.venv\Scripts\pip.exe install [packages]
```

---

## 🚀 Next Steps

### Phase 1: Bronze to Silver Analysis
1. **Execute notebook cells** to analyze bronze layer structure
2. **Map SalesLT tables** to retail model entities
3. **Identify transformation requirements**
4. **Document gaps and challenges**

### Phase 2: Data Transformation
1. **Implement bronze to silver transformations**
2. **Create data quality checks**
3. **Build automated pipelines**
4. **Test with sample data**

### Phase 3: Production Deployment
1. **Deploy to Fabric workspace**
2. **Configure automated scheduling**
3. **Set up monitoring and alerting**
4. **Create operational runbooks**

---

## 📞 Support & Resources

### Documentation
- [Microsoft Fabric Documentation](https://docs.microsoft.com/fabric/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)

### Key Files
- `test_fabric_connection.py` - Environment verification
- `Export_SalesLT_to_Bronze.ipynb` - Working notebook
- `FABRIC_VSCODE_SETUP_GUIDE.md` - Original setup guide
- `COMPLETE_SETUP_GUIDE.md` - This comprehensive guide

### Project Context
- **Objective**: Transform SalesLT data (10 tables) → Retail model (50+ tables)
- **Architecture**: Bronze → Silver → Gold data pipeline
- **Tools**: Microsoft Fabric, VS Code, Python, PySpark

---

## ✅ Setup Verification Checklist

- [ ] VS Code with all required extensions installed
- [ ] Python 3.11.9 virtual environment in `src\.venv`
- [ ] All required packages installed and working
- [ ] Test script runs successfully
- [ ] Notebook kernel works without hanging
- [ ] Project structure organized correctly
- [ ] Documentation created and accessible

---

*This guide was created based on successful setup and testing completed on July 18, 2025. All commands and configurations have been verified to work in the specified environment.*
