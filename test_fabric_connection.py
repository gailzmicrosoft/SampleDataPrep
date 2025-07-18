# Test Microsoft Fabric connection
import pandas as pd
from datetime import datetime

print("🔍 FABRIC VS CODE SETUP TEST")
print("=" * 50)

# Test basic libraries
try:
    print("✅ Pandas imported successfully")
    print(f"📦 Pandas version: {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas import failed: {e}")

# Test Azure libraries
try:
    from azure.identity import DefaultAzureCredential
    from azure.storage.filedatalake import DataLakeServiceClient
    print("✅ Azure libraries imported successfully")
except ImportError as e:
    print(f"❌ Azure libraries import failed: {e}")

# Test PySpark (for local development)
try:
    from pyspark.sql import SparkSession
    print("✅ PySpark imported successfully")
except ImportError as e:
    print(f"❌ PySpark import failed: {e}")

print(f"\n🎯 Test completed at: {datetime.now()}")
print("🚀 Ready for Fabric development!")
print("\nNext Steps:")
print("1. Open Fabric extension in VS Code")
print("2. Sign in to your Fabric workspace")
print("3. Access your bronze and silver lakehouses")
print("4. Open your Bronze_to_Silver_Schema_Analysis.ipynb")
