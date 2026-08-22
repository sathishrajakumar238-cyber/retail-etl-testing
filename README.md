# Retail ETL Testing Project

An end-to-end ETL pipeline and automated test suite built to validate a retail sales data warehouse ? covering source-to-target reconciliation, transformation logic, and Slowly Changing Dimension (SCD Type 2) history tracking.

## Problem Statement

A retail company's sales data lives in a transactional source system. This project builds an ETL pipeline that extracts, transforms, and loads that data into a star-schema data warehouse ? while preserving full historical accuracy for customer data using SCD Type 2 ? and validates every step with an automated test suite.

## Entity Relationship Diagram

\\\mermaid
erDiagram
    dim_customer {
        int customer_key PK
        int customer_id
        varchar name
        varchar address
        varchar city
        date effective_date
        date end_date
        boolean is_current
    }

    dim_product {
        int product_key PK
        int product_id
        varchar sku
        varchar name
        varchar category
        numeric unit_price
    }

    dim_date {
        int date_key PK
        date full_date
        int day
        int month
        int year
        int quarter
    }

    fact_sales {
        int sale_id PK
        int date_key FK
        int customer_key FK
        int product_key FK
        int store_id
        int quantity
        numeric unit_price
        numeric total_amount
    }

    dim_customer ||--o{ fact_sales : "has"
    dim_product ||--o{ fact_sales : "has"
    dim_date ||--o{ fact_sales : "has"
\\\

## Architecture

Source (Postgres: customers, products, orders)
  -> Python ETL (extract.py, transform.py, run_etl.py)
  -> Data Warehouse (Postgres star schema)
  -> Automated tests (pytest + behave)
  -> CI/CD (GitHub Actions)

## Key Features

- **SCD Type 2** implementation for customer history tracking
- **12 automated pytest tests** covering reconciliation, referential integrity, transformation logic, and SCD2 behavior
- **BDD/Gherkin scenarios** using behave for business-readable test cases
- **CI/CD pipeline** via GitHub Actions running the full suite on every push

## How to Run

1. Set up PostgreSQL and create two databases: \etail_source\, \etail_dw\
2. Run the SQL scripts in \sql/\ to create the schemas
3. \pip install -r requirements.txt\
4. \python data/generate_source_data.py\
5. \python etl/populate_dim_date.py\
6. \python etl/run_etl.py\
7. \pytest tests/ -v\
8. \ehave features/\

## Test Coverage

| Test Type | File | What It Validates |
|---|---|---|
| Reconciliation | test_reconciliation.py | Row counts and totals match between source and warehouse |
| Referential Integrity | test_referential_integrity.py | No orphaned foreign keys in fact table |
| SCD2 | test_scd2.py | Customer history is correctly preserved on changes |
| Transformation | test_transformation.py | Calculated fields and business rules are correct |
