import psycopg2
import random
from datetime import datetime, timedelta
import os
import sys
import getpass
import json
from decimal import Decimal

# Adjust these with your own DB connection info
dbhost = "customchatbotdbserver.postgres.database.azure.com"
dbname = "testdb"
sslmode = "prefer"

dbuser = input('Enter your PostgreSQL DB username: ')
password = getpass.getpass(prompt='Enter your PostgreSQL password: ')

conn_string = f"host={dbhost} dbname={dbname} user={dbuser} password={password} sslmode={sslmode}"

# Prompt the user for the customer's first and last name
#customer_first_name = input('Enter the customer\'s first name: ')
#customer_last_name = input('Enter the customer\'s last name: ')

customer_first_name = "Mikaela"
customer_last_name = "Lee"
customer_email = "Mikaela@example.com"

try:
    # Connect to the database
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connection established")

    # Query the orders table for the given customer
    query = """
    SELECT customer_first_name,
           customer_last_name,
           customer_age,
           customer_email,
           customer_phone,
           order_date,
           product_id,
           product_name,           
           quantity,
           unit_price,
           total,
           category,
           brand,
           product_description
    FROM public.orders
    WHERE customer_first_name = %s AND customer_last_name = %s 
    ORDER BY order_date
    LIMIT 3
    """
    cursor.execute(query, (customer_first_name, customer_last_name))
    orders = cursor.fetchall()

    # Convert the orders to a list of dictionaries
    customer_orders = []
    if orders:
        print(f"Orders for {customer_first_name} {customer_last_name}:")
        for order in orders:
            order_dict = {
                "customer_first_name": order[0],
                "customer_last_name": order[1],
                "customer_age": order[2],
                "customer_email": order[3],
                "customer_phone": order[4],
                "order_date": order[5].isoformat(),  # Convert date to string
                "product_id": order[6],
                "product_name": order[7],
                "quantity": order[8],
                "unit_price": float(order[9]),  # Convert Decimal to float
                "total": float(order[10]),  # Convert Decimal to float
                "category": order[11],
                "brand": order[12],
                "product_description": order[13]
            }
            print(order_dict)
            customer_orders.append(order_dict)
    else:
        print(f"No orders found for {customer_first_name} {customer_last_name}")

    conn.commit()
    print("Successfully done.")
except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error: {error}")
    if conn:
        conn.rollback()
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Connection closed")

# Print the customer_orders list
print("Customer Orders List:")
print(json.dumps(customer_orders, indent=4))