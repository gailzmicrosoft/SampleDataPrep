from azure.identity import DefaultAzureCredential
import psycopg2
import os
import pandas as pd

# Configuration parameters
key_vault_name = "key_vault_name_place_holder"
host_name = "host_name_place_holder"
admin_principal_name = "admin_principal_name_place_holder"
identity_name = "identity_name_place_holder"
database_name = "database_name_place_holder"
basrUrl = "basrUrl_place_holder"

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