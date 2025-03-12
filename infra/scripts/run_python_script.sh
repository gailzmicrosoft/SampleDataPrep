#!/bin/bash
echo "started the script"

# Variables
baseUrl="$1"
keyvaultName="$2"
requirementFile="requirements.txt"
requirementFileUrl=${baseUrl}"scripts/data_scripts/requirements.txt"
resourceGroup="$3"
serverName="$4"
principal_name="$5"
admin_principal_name="$6"
additional_principal_name="$7"
managedIdentityName="$8"

echo "Script Started"

# Get the public IP address of the machine running the script
publicIp=$(curl -s https://api.ipify.org)

# Use Azure CLI to add the public IP to the PostgreSQL firewall rule
az postgres flexible-server firewall-rule create --resource-group $resourceGroup --name $serverName --rule-name "AllowScriptIp" --start-ip-address "$publicIp" --end-ip-address "$publicIp"

# Download the create table python file
#curl --output "create_postgres_tables.py" ${baseUrl}"scripts/data_scripts/create_postgres_tables.py"
curl --output "run_psql_script.py" ${baseUrl}"scripts/data_scripts/run_psql_script.py"

# Download the requirement file
curl --output "$requirementFile" "$requirementFileUrl"

echo "Download completed"

#Replace key vault name
sed -i "s/kv_to-be-replaced/${keyvaultName}/g" "run_psql_script.py"
sed -i "s/principal_name/${principal_name}/g" "run_psql_script.py"
sed -i "s/admin_principal_name/${admin_principal_name}/g" "run_psql_script.py"
sed -i "s/user/${user}/g" "run_psql_script.py"
sed -i "s/additional_principal_name/${additional_principal_name}/g" "run_psql_script.py"
sed -i "s/serverName/${serverName}/g" "run_psql_script.py"

pip install -r requirements.txt

#python create_postgres_tables.py
python run_psql_script.py

