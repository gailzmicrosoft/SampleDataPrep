import psycopg2
import pandas as pd
import urllib.parse
import os
import sys
import getpass

# Read URI parameters from the environment
dbhost = "customchatbotdbserver.postgres.database.azure.com"
dbname = "testdb"
sslmode = "prefer"

# Prompt the user for the password securely
dbuser = input('Enter your PostgreSQL DB username: ')
password = getpass.getpass(prompt='Enter your PostgreSQL password: ')

# Connection string
conn_string = f"host={dbhost} dbname={dbname} user={dbuser} password={password} sslmode={sslmode}"

# Connect to the PostgreSQL server
conn = psycopg2.connect(conn_string)
print("Connection established")
cursor = conn.cursor()


# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_directory}")

# Construct the file directory
csv_file_dir = os.path.join(script_directory, 'sample_data')
print(f"CSV file directory: {csv_file_dir}")

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

print("Inserted rows from sample data file into the products table")


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

print("Inserted rows from sample data file into the customers table")

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
print("Inserted rows from sample data file into the orders table")

print("\n\n All Finished. \n")

# Clean up
conn.commit()
cursor.close()
conn.close()