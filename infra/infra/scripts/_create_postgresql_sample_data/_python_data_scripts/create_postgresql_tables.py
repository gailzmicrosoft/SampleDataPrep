import os
import psycopg2
from psycopg2 import sql

# Get environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
sql_file_path = '../postgresql_db_scripts/db_create_tables.sql'  # Updated path

def execute_sql_file(cursor, sql_file):
    with open(sql_file, 'r') as file:
        sql_commands = file.read()
        cursor.execute(sql_commands)

def main():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()
        
        # Execute the SQL file
        execute_sql_file(cursor, sql_file_path)
        
        # Commit the changes
        connection.commit()
        
        print("Tables created successfully.")
        
    except Exception as error:
        print(f"Error: {error}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    main()