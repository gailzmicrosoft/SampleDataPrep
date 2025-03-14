from azure.identity import DefaultAzureCredential
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import os
import pandas as pd

# Configuration parameters
key_vault_name = "your_key_vault_name_here"
# Note: The key vault name is not used in this script, but it's included for completeness.
host_name = "xyz.postgres.database.azure.com"
admin_principal_name = "admin_principal_name_place_holder" # not used in testing
identity_name = "yourAdminUserName" # use an authorized user name here to test the script
database_name = "postgres"
basrUrl = "https://raw.githubusercontent.com/gailzmicrosoft/TestCode/main/infra/"

# look for this line in main program and change to your own value 
#access_token = "Fake_password" #


def truncate_tables(cursor, tables):
    """
    Truncate the specified tables.
    """
    for table in tables:
        cursor.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table)))
    print("Tables truncated: {}".format(", ".join(tables)))

def load_table_from_csv(cursor, table_name, csv_file_path, columns):
    """
    Loads data from a CSV file into a specified PostgreSQL table.
    """
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
    rows = [tuple(row[col] for col in columns) for index, row in df.iterrows()]
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns))
    )
    psycopg2.extras.execute_values(cursor, insert_query, rows)
    print("Data loaded into {} table.".format(table_name))

def main():
    try:
        # Acquire the access token
        print("Acquiring access token...")
        # cred = DefaultAzureCredential()
        # access_token = cred.get_token("https://ossrdbms-aad.database.windows.net/.default")
        # print("Access token acquired.")
        
        print("database: {} server_name: {}".format(database_name, host_name))
        
        # Combine the token with the connection string to establish the connection.
        access_token = "Fake_password" #
        conn_string = (
            "host={0} user={1} dbname={2} password={3} sslmode=require".format(
                host_name, identity_name, database_name, access_token
            )
        )
        
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("Database connection established.")
        
        # Truncate the tables
        truncate_tables(cursor, ["products", "customers", "orders"])
        conn.commit()
        
        # Load data into the products table
        csv_file_path_products = os.path.join(basrUrl, 'data/postgresql_db_sample_data/products.csv')
        load_table_from_csv(cursor, 'products', csv_file_path_products, 
            ['id', 'product_name', 'price', 'category', 'brand', 'product_description'])
        conn.commit()
        
        # Load data into the customers table
        csv_file_path_customers = os.path.join(basrUrl, 'data/postgresql_db_sample_data/customers.csv')
        load_table_from_csv(cursor, 'customers', csv_file_path_customers, 
            ['id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'age', 'email', 'phone', 'post_address', 'membership'])
        conn.commit()
        
        # Load data into the orders table
        csv_file_path_orders = os.path.join(basrUrl, 'data/postgresql_db_sample_data/orders.csv')
        load_table_from_csv(cursor, 'orders', csv_file_path_orders, 
            ['id', 'customer_id', 'product_id', 'quantity', 'total', 'order_date', 'customer_first_name', 'customer_last_name', 'unit_price', 'category', 'brand', 'product_description', 'return_status'])
        conn.commit()
        
    except Exception as e:
        print("An error occurred: {}".format(e))
        conn.rollback()  # Rollback the transaction in case of error
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()