-- SQL script to create tables for a prototype e-commerce PostgreSQL database

-- List existing tables 
-- select table_name from information_schema.tables where table_schema = 'public' and table_type = 'BASE TATBLE'
-- Drop all tables 
-- DROP TABLE IF EXISTS products;
-- DROP TABLE IF EXISTS orders;
-- DROP TABLE IF EXISTS orders;

-- Forcefully drop tables if they exist, including dependent objects
-- DROP TABLE IF EXISTS public.products CASCADE;
-- DROP TABLE IF EXISTS public.customers CASCADE;
-- DROP TABLE IF EXISTS public.orders CASCADE;


-- PostgreSQL script to Truncate all data from tables
-- Truncate Table public.products;
-- Truncate Table public.customers;
-- Truncate Table public.orders;


-- Create the products table
--DROP TABLE IF EXISTS products;
CREATE TABLE IF NOT EXISTS products
(
    id integer,
    product_name character varying(100),
    price numeric(10,2) NOT NULL,
    category character varying(50),
    brand character varying(50),
    product_description text);

-- Create the customers table
--DROP TABLE IF EXISTS customers;
CREATE TABLE customers
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

-- Create the orders table
--DROP TABLE IF EXISTS orders;
CREATE TABLE orders
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
    product_name character varying(100) NOT NULL,
    quantity integer,
    unit_price numeric(10,2),
    total numeric(10,2),
    category character varying(50),
    brand character varying(50),
    product_description text,
    return_status BOOLEAN DEFAULT FALSE
);