from sqlalchemy import text

def test_row_count_orders_vs_fact(source_engine, dw_engine):
    with source_engine.connect() as c:
        src_count = c.execute(text("SELECT COUNT(*) FROM orders")).scalar()
    with dw_engine.connect() as c:
        dw_count = c.execute(text("SELECT COUNT(*) FROM fact_sales")).scalar()
    assert src_count == dw_count, f"Row count mismatch: source={src_count}, fact={dw_count}"

def test_revenue_reconciliation(source_engine, dw_engine):
    with source_engine.connect() as c:
        src_qty = c.execute(text("SELECT SUM(quantity) FROM orders")).scalar()
    with dw_engine.connect() as c:
        dw_qty = c.execute(text("SELECT SUM(quantity) FROM fact_sales")).scalar()
    assert src_qty == dw_qty, f"Quantity mismatch: source={src_qty}, fact={dw_qty}"

def test_no_orphaned_fact_customers(dw_engine):
    with dw_engine.connect() as c:
        orphans = c.execute(text('''
            SELECT COUNT(*) FROM fact_sales f
            LEFT JOIN dim_customer d ON f.customer_key = d.customer_key
            WHERE d.customer_key IS NULL
        ''')).scalar()
    assert orphans == 0, f"Found {orphans} fact rows with no matching customer"
