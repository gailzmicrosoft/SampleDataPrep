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
xslx_file_dir = os.path.join(script_directory, 'sample_data')
print(f"CSV file directory: {xslx_file_dir}")

# Path to the file
xlsx_file_path = os.path.join(xslx_file_dir, 'orders_data.xlsx')
print(f"Excel file path: {xlsx_file_path}")

# Check if the Excel file exists
if not os.path.exists(xlsx_file_path):
    print(f"Excel file does not exist: {xlsx_file_path}")
    sys.exit(1)

# Read the Excel file into a DataFrame, specifying the sheet name
df = pd.read_excel(xlsx_file_path, sheet_name='orders')

# Strip whitespace from column names
df.columns = df.columns.str.strip()
# Insert data into the orders table
for index, row in df.iterrows():
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

# Commit the transaction and close connections
conn.commit()
cursor.close()
conn.close()