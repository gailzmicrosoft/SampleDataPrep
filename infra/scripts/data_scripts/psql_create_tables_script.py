# version 1.1
from azure.identity import DefaultAzureCredential
import psycopg2
from psycopg2 import sql
import logging
import sys
import argparse  # Added for parsing command-line arguments

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Grant Permission Function
def grant_permissions(cursor, db_name, schema_name, principal_name):
    """
    Grants database and schema-level permissions to a specified principal.
    """
    logger.info(f"Granting permissions to principal '{principal_name}' on database '{db_name}' and schema '{schema_name}'.")

    # Check if the principal exists in the database
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = {principal}").format(
            principal=sql.Literal(principal_name)
        )
    )
    if cursor.fetchone() is None:
        logger.info(f"Principal '{principal_name}' does not exist. Creating the principal.")
        add_principal_user_query = sql.SQL(
            "SELECT * FROM pgaadauth_create_principal({principal}, false, false)"
        )
        cursor.execute(
            add_principal_user_query.format(
                principal=sql.Literal(principal_name),
            )
        )
        logger.info(f"Principal '{principal_name}' created successfully.")

    # Grant CONNECT on database
    grant_connect_query = sql.SQL("GRANT CONNECT ON DATABASE {database} TO {principal}")
    cursor.execute(
        grant_connect_query.format(
            database=sql.Identifier(db_name),
            principal=sql.Identifier(principal_name),
        )
    )
    logger.info(f"Granted CONNECT on database '{db_name}' to '{principal_name}'.")

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
    logger.info(f"Granted SELECT, INSERT, UPDATE, DELETE on all tables in schema '{schema_name}' to '{principal_name}'.")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create tables and grant permissions in PostgreSQL.")
    parser.add_argument("--host_name", required=True, help="The hostname of the PostgreSQL server.")
    parser.add_argument("--admin_principal_name", required=True, help="The admin principal name.")
    parser.add_argument("--identity_name", required=True, help="The identity name for database access.")
    parser.add_argument("--database_name", required=True, help="The name of the PostgreSQL database.")
    args = parser.parse_args()

    # Assign arguments to variables
    host_name = args.host_name
    admin_principal_name = args.admin_principal_name
    identity_name = args.identity_name
    database_name = args.database_name
    
    # check any of the arguments are empty or null, if so, raise an error and exit the program
    if not host_name or not admin_principal_name or not identity_name or not database_name:
        logger.error("All arguments are required: --host_name, --admin_principal_name, --identity_name, --database_name")
        sys.exit(1)

    # Log the parameters being used
    logger.info(f"Host Name: {host_name}")
    logger.info(f"Admin Principal Name: {admin_principal_name}")
    logger.info(f"Identity Name: {identity_name}")
    logger.info(f"Database Name: {database_name}")

    logger.info("Starting the script to create tables and grant permissions.")

    try:
        # Acquire the access token
        logger.info("Acquiring access token.")
        cred = DefaultAzureCredential()
        ACCESS_TOKEN_SCOPE = "https://ossrdbms-aad.database.windows.net/.default"
        access_token = cred.get_token(ACCESS_TOKEN_SCOPE)
        logger.info("Access token acquired successfully.")

        # Combine the token with the connection string to establish the connection.
        logger.info("Establishing connection to the database.")
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode=require".format(
            host_name, identity_name, database_name, access_token.token
        )
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        logger.info("Connection established successfully.")

        # Drop and recreate the products table
        logger.info("Dropping and recreating the 'products' table.")
        cursor.execute("DROP TABLE IF EXISTS public.products")
        conn.commit()

        create_products_sql = """
        CREATE TABLE IF NOT EXISTS public.products
        (
            id integer,
            product_name character varying(100),
            price numeric(10,2) NOT NULL,
            category character varying(50),
            brand character varying(50),
            product_description text
        );
        """
        cursor.execute(create_products_sql)
        conn.commit()
        logger.info("'products' table created successfully.")

        # Drop and recreate the customers table
        logger.info("Dropping and recreating the 'customers' table.")
        cursor.execute("DROP TABLE IF EXISTS public.customers")
        conn.commit()

        create_customers_sql = """
        CREATE TABLE IF NOT EXISTS public.customers
        (
            id integer,
            first_name character varying(50),
            last_name character varying(50),
            gender character varying(10),
            date_of_birth date,
            age integer,
            email character varying(100),
            phone character varying(20),
            post_address character varying(255),
            membership character varying(50)
        );
        """
        cursor.execute(create_customers_sql)
        conn.commit()
        logger.info("'customers' table created successfully.")

        # Drop and recreate the orders table
        logger.info("Dropping and recreating the 'orders' table.")
        cursor.execute("DROP TABLE IF EXISTS public.orders")
        conn.commit()

        create_orders_sql = """
        CREATE TABLE IF NOT EXISTS public.orders
        (
            id integer,
            customer_id integer,
            customer_first_name character varying(50),
            customer_last_name character varying(50),
            customer_gender character varying(10),
            customer_age integer,
            customer_email character varying(100),
            customer_phone character varying(20),
            order_date date,
            product_id integer,
            product_name character varying(100),
            quantity integer,
            unit_price numeric(10,2),
            total numeric(10,2),
            category character varying(50),
            brand character varying(50),
            product_description text,
            return_status BOOLEAN DEFAULT FALSE
        );
        """
        cursor.execute(create_orders_sql)
        conn.commit()
        logger.info("'orders' table created successfully.")

        # Grant permissions to the admin principal if provided
        if admin_principal_name and admin_principal_name.strip():
            logger.info(f"Granting permissions to admin principal '{admin_principal_name}'.")
            grant_permissions(cursor, database_name, "public", admin_principal_name)
            conn.commit()

        # Grant permissions to the additional principal if provided
        if identity_name and identity_name.strip():
            logger.info(f"Granting permissions to identity '{identity_name}'.")
            grant_permissions(cursor, database_name, "public", identity_name)
            conn.commit()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logger.info("Database connection closed.")

# Entry point
if __name__ == "__main__":
    main()