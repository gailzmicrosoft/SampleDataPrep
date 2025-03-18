# Define parameters
param (
    [Parameter(Mandatory=$true)]
    [string]$baseUrl,

    [Parameter(Mandatory=$true)]
    [string]$resourceGroup,

    [Parameter(Mandatory=$true)]
    [string]$key_vault_name,

    [Parameter(Mandatory=$true)]
    [string]$postgres_server_name,

    [Parameter(Mandatory=$true)]
    [string]$host_name,

    [Parameter(Mandatory=$true)]
    [string]$database_name,

    [Parameter(Mandatory=$true)]
    [string]$admin_principal_name,

    [Parameter(Mandatory=$true)]
    [string]$identity_name  # managed identity user name. Will use this to connect to the postgres server
)

# Display a message indicating the script has started
Write-Output "started the script"

# Variables
$requirementFile = "requirements.txt"
$requirementFileUrl = "${baseUrl}scripts/data_scripts/requirements_load_tables.txt"

Write-Output "Script Started"

# Get the public IP address of the machine running the script
$publicIp = Invoke-RestMethod -Uri "https://api.ipify.org"

# Use Azure CLI to add the public IP to the PostgreSQL firewall rule
# az postgres flexible-server firewall-rule create --resource-group $resourceGroup --name $postgres_server_name --rule-name "AllowScriptIp" --start-ip-address $publicIp --end-ip-address $publicIp

# Download the Python script
Invoke-WebRequest -Uri "${baseUrl}scripts/data_scripts/run_psql_load_tables_script.py" -OutFile "run_psql_load_tables_script.py"

# Download the requirement file
Invoke-WebRequest -Uri $requirementFileUrl -OutFile $requirementFile

Write-Output "Download completed"
Write-Host "Python script and requirments.txt downloaded"

# # Replace place_holder values in the script with actual values
# (Get-Content "run_psql_load_tables_script.py") -replace "key_vault_name_place_holder", $key_vault_name |
#     Set-Content "run_psql_load_tables_script.py"
# (Get-Content "run_psql_load_tables_script.py") -replace "host_name_place_holder", $host_name |
#     Set-Content "run_psql_load_tables_script.py"
# (Get-Content "run_psql_load_tables_script.py") -replace "database_name_place_holder", $database_name |
#     Set-Content "run_psql_load_tables_script.py"
# (Get-Content "run_psql_load_tables_script.py") -replace "admin_principal_name_place_holder", $admin_principal_name |
#     Set-Content "run_psql_load_tables_script.py"
# (Get-Content "run_psql_load_tables_script.py") -replace "identity_name_place_holder", $identity_name |
#     Set-Content "run_psql_load_tables_script.py"

# Install the required packages
pip install --no-cache-dir -r requirements.txt
Write-Host "Requirements.txt installed"

# Execute Python code
python run_psql_load_tables_script.py --key_vault_name $key_vault_name --host_name $host_name --database_name $database_name --admin_principal_name $admin_principal_name --identity_name $identity_name --baseUrl $baseUrl

Write-Host "Python script executed"