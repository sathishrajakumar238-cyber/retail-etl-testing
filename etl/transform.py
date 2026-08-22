import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

DW_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_dw"


def transform_and_load_customers_scd2(customers_df):
    engine = create_engine(DW_URL)
    with engine.begin() as conn:
        for _, row in customers_df.iterrows():
            existing = conn.execute(
                text("SELECT * FROM dim_customer WHERE customer_id=:cid AND is_current=TRUE"),
                {"cid": row["customer_id"]}
            ).fetchone()

            if existing is None:
                conn.execute(text("""
                    INSERT INTO dim_customer (customer_id, name, address, city, effective_date, is_current)
                    VALUES (:cid, :name, :addr, :city, :eff, TRUE)
                """), {"cid": row["customer_id"], "name": row["name"],
                       "addr": row["address"], "city": row["city"], "eff": date.today()})
            elif existing.address != row["address"] or existing.city != row["city"]:
                conn.execute(text("""
                    UPDATE dim_customer SET end_date=:today, is_current=FALSE
                    WHERE customer_key=:key
                """), {"today": date.today(), "key": existing.customer_key})
                conn.execute(text("""
                    INSERT INTO dim_customer (customer_id, name, address, city, effective_date, is_current)
                    VALUES (:cid, :name, :addr, :city, :eff, TRUE)
                """), {"cid": row["customer_id"], "name": row["name"],
                       "addr": row["address"], "city": row["city"], "eff": date.today()})


def transform_and_load_products(products_df):
    engine = create_engine(DW_URL)
    products_df.to_sql("dim_product_staging", engine, if_exists="replace", index=False)
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO dim_product (product_id, sku, name, category, unit_price)
            SELECT product_id, sku, name, category, unit_price FROM dim_product_staging
            ON CONFLICT DO NOTHING
        """))


def transform_and_load_facts(orders_df):
    engine = create_engine(DW_URL)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE fact_sales"))

    product_map = pd.read_sql("SELECT product_id, product_key, unit_price FROM dim_product", engine)
    customer_map = pd.read_sql("SELECT customer_id, customer_key FROM dim_customer WHERE is_current=TRUE", engine)

    merged = orders_df.merge(product_map, on="product_id").merge(customer_map, on="customer_id")
    merged["total_amount"] = merged["quantity"] * merged["unit_price"]
    merged["date_key"] = pd.to_datetime(merged["order_date"]).dt.strftime("%Y%m%d").astype(int)

    fact = merged[["date_key", "customer_key", "product_key", "store_id", "quantity", "unit_price", "total_amount"]]
    fact.to_sql("fact_sales", engine, if_exists="append", index=False)
