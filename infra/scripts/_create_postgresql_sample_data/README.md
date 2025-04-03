## PostgreSQL and Python Scripts  
This folder contains PostgreSQL and Python Scripts to set up database, create users, grant permissions, create tables, and populate tables with prepared sample data. 

#### Order of Execution

(1) Create Azure PostgreSQL Server (You can use pgAdmin or other tools)

(2) Create Database 

(3) Create Tables: `_postgresql_db_scripts\db_create_tables.sql`

(4) Upload sample data to tables using Python Scripts in folder **_python_data_scripts**: 

- run **either** `populate_all_tables.py` **or** `populate_all_tables_from_xlsx.py` (Do not run both scripts, otherwise you will duplicate the data insertions)

There are more scripts in the folder `python_data_scripts` for individual tables. These are useful for additional data processing or debugging one table. 

(5) Check data populated in PostgreSQL database. 

