-- ============================================================
-- Hive Table Definitions for E-Commerce Data Warehouse
-- Star Schema: Fact + Dimension Tables
-- ============================================================

CREATE DATABASE IF NOT EXISTS ecommerce_dw;
USE ecommerce_dw;

-- Dimension: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id     STRING,
    name            STRING,
    email           STRING,
    region          STRING,
    signup_date     DATE,
    platform        STRING
)
STORED AS PARQUET;

-- Dimension: Products
CREATE TABLE IF NOT EXISTS dim_products (
    product_id      STRING,
    name            STRING,
    category        STRING,
    price           DOUBLE,
    brand           STRING
)
STORED AS PARQUET;

-- Dimension: Dates
CREATE TABLE IF NOT EXISTS dim_dates (
    date_id         INT,
    date            DATE,
    year            INT,
    month           INT,
    day             INT,
    quarter         INT,
    day_of_week     INT,
    week_of_year    INT,
    is_weekend      BOOLEAN
)
STORED AS PARQUET;

-- Fact: Orders (Partitioned by year and month)
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id        STRING,
    customer_id     STRING,
    product_id      STRING,
    date_id         INT,
    quantity         INT,
    unit_price      DOUBLE,
    total_amount    DOUBLE,
    status          STRING,
    order_date      DATE
)
PARTITIONED BY (order_year INT, order_month INT)
STORED AS PARQUET;
