"""
ETL Pipeline: Google Cloud Storage to BigQuery
Loads, validates, and transforms data into BigQuery partitioned tables.
"""

import logging
from google.cloud import bigquery
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = "your-gcp-project-id"
DATASET_ID = "enterprise_analytics"
BUCKET_NAME = "your-data-bucket"


def create_bigquery_client():
    """Create BigQuery client."""
    return bigquery.Client(project=PROJECT_ID)


def create_dataset(client):
    """Create BigQuery dataset if not exists."""
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset, exists_ok=True)
    logger.info(f"Dataset {DATASET_ID} ready")


def load_csv_to_bigquery(client, table_name, gcs_uri, schema):
    """Load CSV from GCS to BigQuery with schema."""
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="order_date"
        ) if "order" in table_name else None
    )

    load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()

    table = client.get_table(table_ref)
    logger.info(f"Loaded {table.num_rows} rows into {table_name}")


def run_transformation(client):
    """Run transformation queries in BigQuery."""
    transform_query = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.sales_summary` AS
    SELECT
        DATE(order_date) as date,
        region,
        category,
        COUNT(DISTINCT order_id) as total_orders,
        COUNT(DISTINCT customer_id) as unique_customers,
        ROUND(SUM(total_amount), 2) as revenue,
        ROUND(AVG(total_amount), 2) as avg_order_value
    FROM `{PROJECT_ID}.{DATASET_ID}.fact_orders` f
    JOIN `{PROJECT_ID}.{DATASET_ID}.dim_customers` c USING(customer_id)
    JOIN `{PROJECT_ID}.{DATASET_ID}.dim_products` p USING(product_id)
    WHERE status = 'completed'
    GROUP BY date, region, category
    """

    job = client.query(transform_query)
    job.result()
    logger.info("Transformation complete: sales_summary table created")


def main():
    """Main ETL pipeline."""
    logger.info("Starting GCP BigQuery ETL Pipeline")

    client = create_bigquery_client()
    create_dataset(client)

    # Load raw data from GCS
    orders_schema = [
        bigquery.SchemaField("order_id", "STRING"),
        bigquery.SchemaField("customer_id", "STRING"),
        bigquery.SchemaField("product_id", "STRING"),
        bigquery.SchemaField("quantity", "INTEGER"),
        bigquery.SchemaField("unit_price", "FLOAT"),
        bigquery.SchemaField("total_amount", "FLOAT"),
        bigquery.SchemaField("order_date", "DATE"),
        bigquery.SchemaField("status", "STRING"),
    ]

    load_csv_to_bigquery(
        client, "fact_orders",
        f"gs://{BUCKET_NAME}/raw/orders.csv",
        orders_schema
    )

    # Run transformations
    run_transformation(client)

    logger.info("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
