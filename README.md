# Batch Data Warehouse on Hadoop

![Stack](https://img.shields.io/badge/Stack-Hive%20%2B%20PySpark%20%2B%20Presto-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

A batch data warehouse built on Hadoop using Apache Hive as the metastore and schema layer, PySpark for ETL processing, and Presto/Trino for fast interactive SQL querying. Processes e-commerce transaction data (orders, customers, products) to support business reporting and growth analysis at scale.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Raw Data (CSV / JSON)                    │
│     Orders, Customers, Products datasets             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              PySpark ETL Jobs                         │
│   Ingest, cleanse, transform, validate               │
│   Apply partitioning and bucketing                   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Apache Hive                              │
│   Metastore and schema layer                         │
│   Star schema: fact + dimension tables               │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Presto / Trino                           │
│   Fast interactive SQL querying                      │
│   Decoupled compute from storage                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Business Reports & Analytics            │
│   Revenue by region, top products, customer trends   │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology | Why Chosen |
|---|---|---|
| Storage | Hadoop HDFS | Distributed storage for large-scale data |
| Metastore | Apache Hive | Schema management and SQL-like querying |
| ETL | PySpark | Scalable data processing with partitioning |
| Query Engine | Presto/Trino | Decouples compute from storage for fast SQL |
| Infrastructure | Docker Compose | Single command setup |

## Data Model (Star Schema)

```
              ┌──────────────┐
              │  dim_products │
              │  product_id   │
              │  category     │
              │  price        │
              └──────┬───────┘
                     │
┌──────────────┐     │     ┌──────────────┐
│ dim_customers │     │     │  dim_dates    │
│ customer_id   ├─────┼─────┤  date_id      │
│ region        │     │     │  year/month   │
│ signup_date   │     │     │  quarter      │
└──────────────┘     │     └──────────────┘
                     │
              ┌──────┴───────┐
              │ fact_orders   │
              │ order_id      │
              │ customer_id   │
              │ product_id    │
              │ date_id       │
              │ amount        │
              │ quantity      │
              └──────────────┘
```

## Project Structure

```
batch-data-warehouse-hadoop/
├── docker-compose.yml           # Hadoop, Hive, Presto setup
├── requirements.txt             # Python dependencies
├── README.md
├── data/
│   └── generate_sample_data.py  # Generate sample e-commerce data
├── etl/
│   └── spark_etl_job.py         # PySpark ETL pipeline
├── hive/
│   └── create_tables.sql        # Hive table definitions (star schema)
└── queries/
    └── business_queries.sql     # Reporting and analytics queries
```

## Quick Start

```bash
git clone https://github.com/santhosh02072k/batch-data-warehouse-hadoop.git
cd batch-data-warehouse-hadoop

docker-compose up -d
pip install -r requirements.txt

python data/generate_sample_data.py
python etl/spark_etl_job.py
```

## Sample Business Queries

- Daily and weekly revenue by region
- Top 10 selling products by category
- Customer retention and repeat purchase rate
- Average order value trends by quarter
- Regional growth analysis

## Author

**Santhosh Ekambaram**
M.S. Computer Science, Illinois Institute of Technology, Chicago

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/santhosh-ekambaram-1457241a2)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github)](https://github.com/santhosh02072k)
