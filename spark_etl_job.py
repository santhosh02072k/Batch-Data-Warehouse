"""
PySpark ETL Job for E-Commerce Data Warehouse
Ingests raw CSV data, applies transformations, and loads into Hive tables.

Pipeline:
1. Read raw CSVs (orders, customers, products)
2. Cleanse and validate data
3. Create dimension tables (dim_customers, dim_products, dim_dates)
4. Create fact table (fact_orders)
5. Apply partitioning and bucketing for optimized queries
"""

import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, FloatType,
    IntegerType, DateType
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
RAW_DATA_PATH = "data/raw"
HIVE_DATABASE = "ecommerce_dw"


def create_spark_session():
    """Create SparkSession with Hive support."""
    return (
        SparkSession.builder
        .appName("ECommerce Data Warehouse ETL")
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.shuffle.partitions", "4")
        .enableHiveSupport()
        .getOrCreate()
    )


def read_raw_data(spark):
    """Read raw CSV files into DataFrames."""
    logger.info("Reading raw data files...")

    orders = spark.read.csv(
        f"{RAW_DATA_PATH}/orders.csv",
        header=True,
        inferSchema=True
    )
    logger.info(f"Orders loaded: {orders.count()} rows")

    customers = spark.read.csv(
        f"{RAW_DATA_PATH}/customers.csv",
        header=True,
        inferSchema=True
    )
    logger.info(f"Customers loaded: {customers.count()} rows")

    products = spark.read.csv(
        f"{RAW_DATA_PATH}/products.csv",
        header=True,
        inferSchema=True
    )
    logger.info(f"Products loaded: {products.count()} rows")

    return orders, customers, products


def cleanse_data(orders, customers, products):
    """Apply data quality checks and cleansing."""
    logger.info("Cleansing data...")

    # Remove nulls in critical fields
    orders_clean = orders.dropna(subset=['order_id', 'customer_id', 'product_id'])

    # Remove duplicate orders
    orders_clean = orders_clean.dropDuplicates(['order_id'])

    # Filter only valid statuses
    valid_statuses = ['completed', 'pending', 'cancelled']
    orders_clean = orders_clean.filter(F.col('status').isin(valid_statuses))

    # Ensure positive amounts
    orders_clean = orders_clean.filter(F.col('total_amount') > 0)

    # Remove duplicate customers and products
    customers_clean = customers.dropDuplicates(['customer_id'])
    products_clean = products.dropDuplicates(['product_id'])

    logger.info(f"After cleansing: {orders_clean.count()} orders, "
                f"{customers_clean.count()} customers, "
                f"{products_clean.count()} products")

    return orders_clean, customers_clean, products_clean


def create_date_dimension(spark, orders):
    """Create date dimension table from order dates."""
    logger.info("Creating date dimension...")

    dates = (
        orders.select(F.col('order_date').alias('date'))
        .distinct()
        .withColumn('date_id', F.date_format('date', 'yyyyMMdd').cast(IntegerType()))
        .withColumn('year', F.year('date'))
        .withColumn('month', F.month('date'))
        .withColumn('day', F.dayofmonth('date'))
        .withColumn('quarter', F.quarter('date'))
        .withColumn('day_of_week', F.dayofweek('date'))
        .withColumn('week_of_year', F.weekofyear('date'))
        .withColumn('is_weekend', F.when(F.dayofweek('date').isin(1, 7), True).otherwise(False))
    )

    logger.info(f"Date dimension: {dates.count()} unique dates")
    return dates


def create_fact_orders(orders):
    """Create fact orders table with date keys."""
    logger.info("Creating fact orders table...")

    fact_orders = (
        orders
        .withColumn('date_id', F.date_format('order_date', 'yyyyMMdd').cast(IntegerType()))
        .withColumn('order_year', F.year('order_date'))
        .withColumn('order_month', F.month('order_date'))
        .select(
            'order_id', 'customer_id', 'product_id', 'date_id',
            'quantity', 'unit_price', 'total_amount', 'status',
            'order_date', 'order_year', 'order_month'
        )
    )

    logger.info(f"Fact orders: {fact_orders.count()} rows")
    return fact_orders


def write_to_hive(spark, df, table_name, partition_cols=None):
    """Write DataFrame to Hive table with optional partitioning."""
    logger.info(f"Writing {table_name} to Hive...")

    spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DATABASE}")

    if partition_cols:
        (
            df.write
            .mode("overwrite")
            .partitionBy(*partition_cols)
            .saveAsTable(f"{HIVE_DATABASE}.{table_name}")
        )
    else:
        (
            df.write
            .mode("overwrite")
            .saveAsTable(f"{HIVE_DATABASE}.{table_name}")
        )

    row_count = spark.sql(f"SELECT count(*) FROM {HIVE_DATABASE}.{table_name}").collect()[0][0]
    logger.info(f"Table {table_name}: {row_count} rows written")


def run_validation(spark):
    """Run basic validation queries on the warehouse."""
    logger.info("Running validation queries...")

    total_orders = spark.sql(
        f"SELECT count(*) as cnt FROM {HIVE_DATABASE}.fact_orders"
    ).collect()[0][0]

    total_revenue = spark.sql(
        f"SELECT round(sum(total_amount), 2) as revenue FROM {HIVE_DATABASE}.fact_orders WHERE status = 'completed'"
    ).collect()[0][0]

    total_customers = spark.sql(
        f"SELECT count(*) as cnt FROM {HIVE_DATABASE}.dim_customers"
    ).collect()[0][0]

    logger.info(f"Validation Results:")
    logger.info(f"  Total orders: {total_orders}")
    logger.info(f"  Total revenue (completed): {total_revenue}")
    logger.info(f"  Total customers: {total_customers}")


def main():
    """Main ETL pipeline."""
    logger.info("Starting E-Commerce Data Warehouse ETL Pipeline")

    spark = create_spark_session()

    # Step 1: Read raw data
    orders, customers, products = read_raw_data(spark)

    # Step 2: Cleanse data
    orders_clean, customers_clean, products_clean = cleanse_data(orders, customers, products)

    # Step 3: Create dimensions
    dim_dates = create_date_dimension(spark, orders_clean)

    # Step 4: Create fact table
    fact_orders = create_fact_orders(orders_clean)

    # Step 5: Write to Hive
    write_to_hive(spark, customers_clean, "dim_customers")
    write_to_hive(spark, products_clean, "dim_products")
    write_to_hive(spark, dim_dates, "dim_dates")
    write_to_hive(spark, fact_orders, "fact_orders", partition_cols=["order_year", "order_month"])

    # Step 6: Validate
    run_validation(spark)

    logger.info("ETL Pipeline completed successfully!")
    spark.stop()


if __name__ == "__main__":
    main()
