-- Run this script to initialize all service databases
-- Usage: docker exec -i some-postgres psql -U postgres -f /init-db.sql

SELECT 'CREATE DATABASE staff_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'staff_db')\gexec
SELECT 'CREATE DATABASE manager_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'manager_db')\gexec
SELECT 'CREATE DATABASE customer_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'customer_db')\gexec
SELECT 'CREATE DATABASE catalog_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'catalog_db')\gexec
SELECT 'CREATE DATABASE book_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'book_db')\gexec
SELECT 'CREATE DATABASE cart_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cart_db')\gexec
SELECT 'CREATE DATABASE order_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'order_db')\gexec
SELECT 'CREATE DATABASE ship_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ship_db')\gexec
SELECT 'CREATE DATABASE pay_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pay_db')\gexec
SELECT 'CREATE DATABASE comment_rate_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'comment_rate_db')\gexec
SELECT 'CREATE DATABASE recommender_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'recommender_db')\gexec
