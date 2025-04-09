-- Define the database name and user variables
DO
$$
DECLARE
    db_name CONSTANT text := 'chatbotdb';
    db_user CONSTANT text := 'dbuser';
    db_user_password CONSTANT text := 'chatbot_db_user_password'; -- Replace this with yours
BEGIN
    -- Create a new user if it does not already exist
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = db_user 
    ) THEN
        EXECUTE format('CREATE USER %I WITH PASSWORD %L', db_user, db_user_password);
    END IF;

    -- Create a new database if it does not already exist
    IF NOT EXISTS (
        SELECT FROM pg_database
        WHERE datname = db_name
    ) THEN
        EXECUTE format('CREATE DATABASE %I', db_name);
    END IF;
END
$$ LANGUAGE plpgsql;

-- Grant access to the database
GRANT CONNECT ON DATABASE chatbotdb TO dbuser;

-- Grant INSERT, UPDATE, DELETE, and SELECT privileges on all tables in the public schema
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA public TO dbuser;

-- Optionally, grant USAGE on the schema if not already granted
GRANT USAGE ON SCHEMA public TO dbuser;

-- If you want to grant permissions on future tables as well
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE, DELETE, SELECT ON TABLES TO dbuser;
