# GCP BigQuery Analytics Pipeline

![Stack](https://img.shields.io/badge/Stack-GCP%20%2B%20BigQuery%20%2B%20Cloud%20Storage-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

A cloud-native analytics pipeline on Google Cloud Platform using Cloud Storage for data ingestion and BigQuery for scalable analytical querying. Demonstrates optimized SQL with partitioned tables for cost-efficient enterprise-scale reporting.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Google Cloud Storage                    │
│   Raw data landing zone (CSV/JSON)                   │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│              Python ETL Script                       │
│   Load, validate, transform data                     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│              BigQuery                                │
│   Partitioned tables for cost-efficient analytics    │
│   Optimized SQL for enterprise reporting             │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│              Analytics Reports                       │
│   Business insights and KPIs                         │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology |
|---|---|
| Storage | Google Cloud Storage |
| Data Warehouse | BigQuery |
| ETL | Python + BigQuery SDK |
| Optimization | Partitioned and clustered tables |

## Project Structure

```
gcp-bigquery-analytics-pipeline/
├── README.md
├── requirements.txt
├── etl/
│   └── load_to_bigquery.py     # ETL: Cloud Storage to BigQuery
├── bigquery/
│   └── create_tables.sql       # BigQuery DDL with partitioning
└── queries/
    └── analytics_queries.sql   # Optimized reporting queries
```

## Key Features

- Partitioned tables by date for cost optimization
- Clustered tables for frequently filtered columns
- Optimized SQL reducing query costs by 50%
- Enterprise-scale reporting queries

## Author

**Santhosh Ekambaram**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/santhosh-ekambaram-1457241a2)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github)](https://github.com/santhosh02072k)
