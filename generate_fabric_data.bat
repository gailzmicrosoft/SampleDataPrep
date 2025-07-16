@echo off
echo ========================================
echo Microsoft Fabric Retail Data Generator
echo ========================================
echo.

echo Installing required packages...
pip install -r requirements_fabric.txt
echo.

echo Generating enhanced sample data...
python fabric_sample_data_generator.py
echo.

echo Running data pipeline transformations...
python fabric_retail_pipeline.py
echo.

echo ========================================
echo Generation Complete!
echo ========================================
echo.
echo Generated outputs:
echo   📁 fabric_enhanced_data/     - Enhanced sample datasets
echo   📁 fabric_data_output/       - Bronze-Silver-Gold layers
echo.
echo Next steps:
echo   1. Review generated data files
echo   2. Upload to Microsoft Fabric Lakehouse
echo   3. Create semantic models and reports
echo.
pause
