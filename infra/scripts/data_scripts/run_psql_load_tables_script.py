from azure.identity import DefaultAzureCredential
import psycopg2
from psycopg2 import sql
# for data loading 
import os
import pandas as pd


key_vault_name = "key_vault_name_place_holder"
host_name = "host_name_place_holder"
admin_principal_name = "admin_principal_name_place_holder"
identity_name = "identity_name_place_holder"
database_name= "database_name_place_holder"
basrUrl = "basrUrl_place_holder"


# Grant Permission Function
def grant_permissions(cursor, db_name, schema_name, principal_name):
    """
    Grants database and schema-level permissions to a specified principal.
    Parameters:
    - cursor: psycopg2 cursor object for database operations.
    - db_name: Name of the database to grant CONNECT permission.
    - schema_name: Name of the schema to grant table-level permissions.
    - principal_name: Name of the principal (role or user) to grant permissions.
    """
    # Check if the principal exists in the database
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = {principal}").format(
            principal=sql.Literal(principal_name)
        )
    )
    if cursor.fetchone() is None:
        add_principal_user_query = sql.SQL(
            "SELECT * FROM pgaadauth_create_principal({principal}, false, false)"
        )
        cursor.execute(
            add_principal_user_query.format(
                principal=sql.Literal(principal_name),
            )
        )

    # Grant CONNECT on database
    grant_connect_query = sql.SQL("GRANT CONNECT ON DATABASE {database} TO {principal}")
    cursor.execute(
        grant_connect_query.format(
            database=sql.Identifier(db_name),
            principal=sql.Identifier(principal_name),
        )
    )
    print(f"Granted CONNECT on database '{db_name}' to '{principal_name}'")

    # Grant SELECT, INSERT, UPDATE, DELETE on schema tables
    grant_permissions_query = sql.SQL(
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA {schema} TO {principal}"
    )
    cursor.execute(
        grant_permissions_query.format(
            schema=sql.Identifier(schema_name),
            principal=sql.Identifier(principal_name),
        )
    )
# end of grant_permissions function

def load_tables(cursor, csv_file_dir):
    """
    load tables from the data files in this directory basrUrl/data/postgresql_db_sample_data
    example basrUrl: 'https://raw.githubusercontent.com/gitHubUserName/RepositoryName/main/infra/'
    csv_file_dir: 'https://raw.githubusercontent.com/gitHubUserName/RepositoryName/main/infra/data/postgresql_db_sample_data'
    data files are:
    - products.csv
    - orders.csv
    - customers.csv
    """
    # Path to the file
    csv_file_path_products = os.path.join(csv_file_dir, 'products.csv')
    csv_file_path_orders = os.path.join(csv_file_dir, 'orders.csv')
    csv_file_path_customers = os.path.join(csv_file_dir, 'customers.csv')

    # Read the CSV file into a DataFrame
    df_products = pd.read_csv(csv_file_path_products)
    df_orders = pd.read_csv(csv_file_path_orders)
    df_customers = pd.read_csv(csv_file_path_customers)

    # Strip whitespace from column names
    df_products.columns = df_products.columns.str.strip()
    df_customers.columns = df_customers.columns.str.strip()
    df_orders.columns = df_orders.columns.str.strip()
    
        # Insert data into the products table
    for index, row in df_products.iterrows():
        cursor.execute(
            "INSERT INTO products (id, product_name, price, category, brand, product_description) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                row['id'],
                row['product_name'],
                row['price'],
                row['category'],
                row['brand'],
                row['product_description']
            )
        )
        
        
        # Insert data into the customers table
    for index, row in df_customers.iterrows():
        cursor.execute(
            "INSERT INTO customers (id, first_name, last_name, gender, date_of_birth, age, email, phone, post_address, membership) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                row['id'],
                row['first_name'],
                row['last_name'],
                row['gender'],
                row['date_of_birth'],
                row['age'],
                row['email'],
                row['phone'],
                row['post_address'],
                row['membership']
            )
        )
    #
    # Insert data into the orders table
    for index, row in df_orders.iterrows():
        cursor.execute(
            "INSERT INTO public.orders (id, customer_id, product_id, quantity, total, order_date, customer_first_name, customer_last_name, unit_price, category, brand, product_description, return_status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                row['id'],
                row['customer_id'],
                row['product_id'],
                row['quantity'],
                row['total'],
                row['order_date'],
                row['customer_first_name'],
                row['customer_last_name'],
                row['unit_price'],
                row['category'],
                row['brand'],
                row['product_description'],
                row['return_status']
            )
        )
        
    # Commit the changes to the database
    conn.commit()
    print("Data loaded successfully into the tables.")
    
##########################################################################################
# Program starts here
##########################################################################################
# Acquire the access token
cred = DefaultAzureCredential()
access_token = cred.get_token("https://ossrdbms-aad.database.windows.net/.default")

# Combine the token with the connection string to establish the connection.
# The identity name is used as the username in the connection string.
conn_string = "host={0} user={1} dbname={2} password={3} sslmode=require".format(
    host_name, identity_name, database_name, access_token.token
)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

csv_file_path = os.path.join(basrUrl, 'data/postgresql_db_sample_data')
load_tables(cursor, csv_file_path)

cursor.close()
conn.close()
