

-- Grant access to the database
GRANT CONNECT ON DATABASE sample_database_name TO dbuser;

-- Grant INSERT, UPDATE, DELETE, and SELECT privileges on all tables in the public schema
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA public TO dbuser;

-- Optionally, grant USAGE on the schema if not already granted
GRANT USAGE ON SCHEMA public TO dbuser;

-- If you want to grant permissions on future tables as well
--ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE, DELETE, SELECT ON TABLES TO dbuser;