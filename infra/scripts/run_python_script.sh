#!/bin/bash
echo "started the script"

# Variables
baseUrl="$1"
key_vault_name="$2"
requirementFile="requirements.txt"
requirementFileUrl=${baseUrl}"scripts/data_scripts/requirements.txt"
resourceGroup="$3"
postgres_server_name="$4"
host_name="$5"
principal_name="$6" # managed identity name 
admin_principal_name="$7"
additional_principal_name="$8"
user_name="$9"  # managed identity user name. Wil use this to connect to the postgres server 


echo "Script Started"

# Get the public IP address of the machine running the script
publicIp=$(curl -s https://api.ipify.org)

# Use Azure CLI to add the public IP to the PostgreSQL firewall rule
# az postgres flexible-server firewall-rule create --resource-group $resourceGroup --name $postgres_server_name --rule-name "AllowScriptIp" --start-ip-address "$publicIp" --end-ip-address "$publicIp"

curl --output "run_psql_script.py" ${baseUrl}"scripts/data_scripts/run_psql_script.py"

# Download the requirement file
curl --output "$requirementFile" "$requirementFileUrl"

echo "Download completed"

#Replace key vault name
sed -i "s/key_vault_name_place_holder/${key_vault_name}/g" "run_psql_script.py"
sed -i "s/principal_name_place_holder/${principal_name}/g" "run_psql_script.py"
sed -i "s/host_name_place_holder/${host_name}/g" "run_psql_script.py"
sed -i "s/principal_name_place_holder/${principal_name}/g" "run_psql_script.py"
sed -i "s/admin_principal_name_place_holder/${admin_principal_name}/g" "run_psql_script.py"
sed -i "s/additional_principal_name_place_holder/${additional_principal_name}/g" "run_psql_script.py"
sed -i "s/user_name_place_holder/${user_name}/g" "run_psql_script.py"

# Create a virtual environment
python -m venv myvenv
source myvenv/bin/activate

pip install -r requirements.txt

# execute python code
python run_psql_script.py

# Deactivate the virtual environment
deactivate

