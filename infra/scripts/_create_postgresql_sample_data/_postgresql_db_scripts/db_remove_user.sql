-- Reassign all objects owned by the user to another user (e.g., postgres)
REASSIGN OWNED BY sample_user_name TO postgres;

-- Drop all objects owned by the user
DROP OWNED BY sample_user_name;

-- Terminate any active connections the user has
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT pg_terminate_backend(pg_stat_activity.pid)
              FROM pg_stat_activity
              WHERE pg_stat_activity.usename = 'sample_user_name') 
    LOOP
        -- Do nothing, just terminate the connections
    END LOOP;
END $$;

-- Drop the user
DROP USER sample_user_name;