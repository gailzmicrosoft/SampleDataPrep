#!/bin/bash
echo "started the script"


# Variables

baseUrl="$1"
resourceGroup="$2"
key_vault_name="$3"
postgres_server_name="$4"
host_name="$5"
database_name="$6"
admin_principal_name="$7"
identity_name="$8"  # managed identity user name. Wil use this to connect to the postgres server 
requirementFile="requirements.txt"
requirementFileUrl=${baseUrl}"scripts/data_scripts/requirements.txt"

echo "Script Started"

# Get the public IP address of the machine running the script
publicIp=$(curl -s https://api.ipify.org)

# Use Azure CLI to add the public IP to the PostgreSQL firewall rule
az postgres flexible-server firewall-rule create --resource-group $resourceGroup --name $postgres_server_name --rule-name "AllowScriptIp" --start-ip-address "$publicIp" --end-ip-address "$publicIp"

curl --output "run_psql_script.py" ${baseUrl}"scripts/data_scripts/run_psql_script.py"

# Download the requirement file
curl --output "$requirementFile" "$requirementFileUrl"

echo "Download completed"

#Replace key vault name
sed -i "s/key_vault_name_place_holder/${key_vault_name}/g" "run_psql_script.py"
sed -i "s/host_name_place_holder/${host_name}/g" "run_psql_script.py"
sed -i "s/database_name_place_holder/${database_name}/g" "run_psql_script.py"
sed -i "s/admin_principal_name_place_holder/${admin_principal_name}/g" "run_psql_script.py"
sed -i "s/identity_name_place_holder/${identity_name}/g" "run_psql_script.py"


# # Create a virtual environment
# python3 -m venv myvenv

# # Check if the virtual environment was created successfully
# if [ -d "myvenv" ]; then
#     echo "Virtual environment created successfully"
# else
#     echo "Failed to create virtual environment"
#     exit 1
# fi

# # Activate the virtual environment
# if [ -f "myvenv/bin/activate" ]; then
#     source myvenv/bin/activate
# elif [ -f "myvenv/Scripts/activate" ]; then
#     source myvenv/Scripts/activate
# else
#     echo "Failed to find the virtual environment activation script"
#     exit 1
# fi

pip install -r requirements.txt

# execute python code
python run_psql_script.py

# # Deactivate the virtual environment
# if [ -f "myvenv/bin/deactivate" ]; then
#     source myvenv/bin/deactivate
# elif [ -f "myvenv/Scripts/deactivate" ]; then
#     source myvenv/Scripts/deactivate
# else
#     echo "Failed to find the virtual environment deactivation script"
#     exit 1
# fi

