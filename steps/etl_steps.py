import os
import sys
import subprocess
from behave import given, when, then
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

engine_source = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_source")
engine_dw = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_dw")

@given('the source orders table has {count:d} records')
def step_check_source_count(context, count):
    with engine_source.connect() as c:
        actual = c.execute(text("SELECT COUNT(*) FROM orders")).scalar()
    assert actual == count, f"Expected {count} orders, found {actual}"

@when('the ETL pipeline runs')
def step_run_etl(context):
    subprocess.run([sys.executable, "etl/run_etl.py"], check=True, cwd=".")

@then('the fact_sales table should have {count:d} records')
def step_check_fact_count(context, count):
    with engine_dw.connect() as c:
        actual = c.execute(text("SELECT COUNT(*) FROM fact_sales")).scalar()
    assert actual == count, f"Expected {count} fact rows, found {actual}"
