from azure.identity import DefaultAzureCredential
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import os
import pandas as pd

# Configuration parameters
key_vault_name = "key_vault_name_place_holder"
host_name = "host_name_place_holder"
admin_principal_name = "admin_principal_name_place_holder"
identity_name = "identity_name_place_holder"
database_name = "database_name_place_holder"
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

def load_table_from_csv(cursor, table_name, csv_file_path, columns):
    """
    Loads data from a CSV file into a specified PostgreSQL table.
    
    Parameters:
    - cursor: psycopg2 cursor object for database operations.
    - table_name: Name of the PostgreSQL table to load data into.
    - csv_file_path: Path to the CSV file containing the data.
    - columns: List of column names in the table.
    """
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
    rows = [tuple(row[col] for col in columns) for index, row in df.iterrows()]
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
    psycopg2.extras.execute_values(cursor, insert_query, rows)

def load_tables(conn, cursor, csv_file_paths):
    """
    Loads data from CSV files into PostgreSQL tables.
    
    Parameters:
    - conn: psycopg2 connection object.
    - cursor: psycopg2 cursor object for database operations.
    - csv_file_paths: Dictionary containing the paths to the CSV files.
    """
    # Load data into the products table
    print("Loading data into the products table...")
    load_table_from_csv(
        cursor, 'products', csv_file_paths['products'], 
        ['id', 'product_name', 'price', 'category', 'brand', 'product_description']
    )
    conn.commit()
    print("Data loaded successfully into the products table.")

    # Load data into the customers table
    print("Loading data into the customers table...")
    load_table_from_csv(
        cursor, 'customers', csv_file_paths['customers'], 
        [
            'id', 'first_name', 'last_name', 'gender', 'date_of_birth', 
            'age', 'email', 'phone', 'post_address', 'membership'
        ]
    )
    conn.commit()
    print("Data loaded successfully into the customers table.")

##########################################################################################
# Program starts here
##########################################################################################
try:
    # Acquire the access token
    print("Acquiring access token...")
    cred = DefaultAzureCredential()
    access_token = cred.get_token("https://ossrdbms-aad.database.windows.net/.default")
    print("Access token acquired.")
    
    # Combine the token with the connection string to establish the connection.
    print("Establishing database connection...")
    conn_string = (
        "host={0} user={1} dbname={2} password={3} sslmode=require".format(
            host_name, identity_name, database_name, access_token.token
        )
    )
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Database connection established.")
    
           
    # Grant permissions to the additional principal if provided
    if identity_name and identity_name.strip():
        grant_permissions(cursor, database_name, "public", identity_name)
        conn.commit()

    # Construct the paths to the CSV files
    csv_file_paths = {
        'customers': os.path.join(basrUrl, 'data/postgresql_db_sample_data', 'customers.csv')
    }

    # Construct the paths to the CSV files
    # csv_file_paths = {
    #     'products': os.path.join(basrUrl, 'data/postgresql_db_sample_data', 'products.csv'),
    #     'customers': os.path.join(basrUrl, 'data/postgresql_db_sample_data', 'customers.csv'),
    #     'orders': os.path.join(basrUrl, 'data/postgresql_db_sample_data', 'orders.csv')
    # }
    

    # Load tables
    load_tables(conn, cursor, csv_file_paths)

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()  # Rollback the transaction in case of error
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()