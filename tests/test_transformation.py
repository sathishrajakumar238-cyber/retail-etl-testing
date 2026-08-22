from sqlalchemy import text

def test_total_amount_calculation(dw_engine):
    with dw_engine.connect() as c:
        bad_rows = c.execute(text('''
            SELECT COUNT(*) FROM fact_sales
            WHERE ROUND(total_amount, 2) != ROUND(quantity * unit_price, 2)
        ''')).scalar()
    assert bad_rows == 0, f"{bad_rows} rows have incorrect total_amount"

def test_no_negative_or_zero_quantities(dw_engine):
    with dw_engine.connect() as c:
        bad = c.execute(text("SELECT COUNT(*) FROM fact_sales WHERE quantity <= 0")).scalar()
    assert bad == 0, f"{bad} rows have invalid quantity"

def test_no_null_prices_in_products(dw_engine):
    with dw_engine.connect() as c:
        bad = c.execute(text("SELECT COUNT(*) FROM dim_product WHERE unit_price IS NULL")).scalar()
    assert bad == 0, f"{bad} products have a null price"

def test_no_duplicate_products(dw_engine):
    with dw_engine.connect() as c:
        dupes = c.execute(text('''
            SELECT product_id, COUNT(*) FROM dim_product
            GROUP BY product_id HAVING COUNT(*) > 1
        ''')).fetchall()
    assert len(dupes) == 0, f"Duplicate products found: {dupes}"
