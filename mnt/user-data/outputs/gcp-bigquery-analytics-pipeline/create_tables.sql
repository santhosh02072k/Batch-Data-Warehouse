-- BigQuery Table Definitions with Partitioning and Clustering

CREATE TABLE IF NOT EXISTS enterprise_analytics.fact_orders (
    order_id STRING,
    customer_id STRING,
    product_id STRING,
    quantity INT64,
    unit_price FLOAT64,
    total_amount FLOAT64,
    order_date DATE,
    status STRING
)
PARTITION BY order_date
CLUSTER BY customer_id, product_id;

CREATE TABLE IF NOT EXISTS enterprise_analytics.dim_customers (
    customer_id STRING,
    name STRING,
    region STRING,
    segment STRING,
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS enterprise_analytics.dim_products (
    product_id STRING,
    name STRING,
    category STRING,
    price FLOAT64,
    brand STRING
);
