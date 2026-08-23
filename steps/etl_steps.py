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

@given('customer 1 has a current address on file')
def step_check_customer_exists(context):
    with engine_dw.connect() as c:
        row = c.execute(text("SELECT * FROM dim_customer WHERE customer_id=1 AND is_current=TRUE")).fetchone()
    assert row is not None, "Expected an existing current record for customer 1"

@when('the customer address is updated in the source system')
def step_update_address(context):
    with engine_source.connect() as c:
        c.execute(text("UPDATE customers SET address='77 BDD Test Lane', city='Waterford' WHERE customer_id=1"))
        c.commit()

@then('the previous address record should be marked as not current')
def step_check_old_record_expired(context):
    with engine_dw.connect() as c:
        rows = c.execute(text("SELECT * FROM dim_customer WHERE customer_id=1 ORDER BY effective_date")).fetchall()
    assert rows[-2].is_current is False, "Expected the previous record to be marked not current"

@then('a new current record should exist with the updated address')
def step_check_new_record_current(context):
    with engine_dw.connect() as c:
        row = c.execute(text("SELECT * FROM dim_customer WHERE customer_id=1 AND is_current=TRUE")).fetchone()
    assert row.address == '77 BDD Test Lane', f"Expected updated address, got {row.address}"

@given('the ETL pipeline has run')
def step_etl_already_ran(context):
    subprocess.run([sys.executable, "etl/run_etl.py"], check=True, cwd=".")

@then('each customer should have exactly one current record in the warehouse')
def step_check_one_current_per_customer(context):
    with engine_dw.connect() as c:
        violations = c.execute(text("""
            SELECT customer_id, COUNT(*) FROM dim_customer
            WHERE is_current=TRUE GROUP BY customer_id HAVING COUNT(*) > 1
        """)).fetchall()
    assert len(violations) == 0, f"Found customers with multiple current records: {violations}"

@then('every sale total should equal quantity multiplied by unit price')
def step_check_totals(context):
    with engine_dw.connect() as c:
        bad = c.execute(text("""
            SELECT COUNT(*) FROM fact_sales
            WHERE ROUND(total_amount, 2) != ROUND(quantity * unit_price, 2)
        """)).scalar()
    assert bad == 0, f"{bad} rows have incorrect totals"

@then('every fact record should reference a valid product')
def step_check_valid_products(context):
    with engine_dw.connect() as c:
        orphans = c.execute(text("""
            SELECT COUNT(*) FROM fact_sales f
            LEFT JOIN dim_product p ON f.product_key = p.product_key
            WHERE p.product_key IS NULL
        """)).scalar()
    assert orphans == 0

@then('every fact record should reference a valid customer')
def step_check_valid_customers(context):
    with engine_dw.connect() as c:
        orphans = c.execute(text("""
            SELECT COUNT(*) FROM fact_sales f
            LEFT JOIN dim_customer d ON f.customer_key = d.customer_key
            WHERE d.customer_key IS NULL
        """)).scalar()
    assert orphans == 0