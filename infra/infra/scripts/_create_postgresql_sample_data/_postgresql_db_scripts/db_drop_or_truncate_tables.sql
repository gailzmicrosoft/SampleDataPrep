-- List existing tables 
-- select table_name from information_schema.tables where table_schema = 'public' and table_type = 'BASE TATBLE'

-- PostgreSQL script to drop tables
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orders;

-- Forcefully drop tables if they exist, including dependent objects
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.customers CASCADE;
DROP TABLE IF EXISTS public.orders CASCADE;


-- PostgreSQL script to Truncate all data from tables
Truncate Table public.products;
Truncate Table public.customers;
Truncate Table public.orders;
