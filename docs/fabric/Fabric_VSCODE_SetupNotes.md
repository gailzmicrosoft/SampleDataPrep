## **Quick Setup Guide:**

### **Step 1: Install Extensions**

Install the essential extensions above - VS Code will handle dependencies automatically.

### **Step 2: Sign In**

- After installing, restart VS Code
- You'll see new Fabric panels in the sidebar
- Click **Sign In** and authenticate with your Microsoft/Azure credentials
- Select your Fabric workspace: `RDS_Fabric_Foundry_workspace_Gaiye_Retail_Solution_Test`

### **Step 3: Verify Connection**

- Open the Fabric panel and confirm you can see:
  - Your bronze lakehouse: `IDM_LH_bronze`
  - Your silver lakehouse: `LH_silver`
  - Your existing notebooks

### **Step 4: Configure Python for Fabric**



src\.venv\Scripts\pip.exe install azure-storage-file-datalake azure-identity pyspark pandas pyarrow delta-spark

Input

{

 "resourcePath": "c:\\Repos\\Code\\SampleDataPrep\src"

}

Output



A Python Environment has been configured.  

Following is the information about the Python environment:

1. Environment Type: VirtualEnvironment
2. Version: 3.11.9.final.0
3. Command Prefix to run Python in a terminal is: `C:/Repos/Code/SampleDataPrep/src/.venv/Scripts/python.exe`

Instead of running `Python sample.py` in the terminal, you will now run: `C:/Repos/Code/SampleDataPrep/.venv/Scripts/python.exe sample.py`

Similarly instead of running `Python -c "import sys;...."` in the terminal, you will now run: `C:/Repos/Code/SampleDataPrep/src/.venv/Scripts/python.exe -c "import sys;...."`



Excellent! Your Fabric development environment is fully set up and working.

## **✅ Setup Complete Summary:**

### **Installed Extensions:**

- ✅ Microsoft Fabric - Core Fabric development
- ✅ Fabric Data Engineering VS Code - Notebooks and Spark
- ✅ SQL Server (mssql) - SQL development
- ✅ Fabric Studio - Enhanced workspace management
- ✅ Python & Jupyter - Already installed for notebook support

### **Python Environment:**

- ✅ Python 3.11.9 virtual environment configured
- ✅ Azure libraries installed (storage, identity)
- ✅ PySpark and data processing libraries ready
- ✅ Connection test passed

### **Next Steps:**

1. **Open Fabric Panel** - Look for the Fabric icon in VS Code sidebar
2. **Sign In** - Use your Microsoft credentials to access your workspace
3. **Connect to Workspace** - Select `RDS_Fabric_Foundry_workspace_Gaiye_Retail_Solution_Test`
4. **Access Lakehouses** - Verify you can see bronze and silver lakehouses
5. **Open Your Analysis Notebook** - Start with `Bronze_to_Silver_Schema_Analysis.ipynb`

You're now ready to execute your customer transformation (Phase 1) directly from VS Code! The Fabric extensions will give you seamless access to your workspace, notebooks, and data processing capabilities.