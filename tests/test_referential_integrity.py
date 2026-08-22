from sqlalchemy import text

def test_fact_product_keys_valid(dw_engine):
    with dw_engine.connect() as c:
        orphans = c.execute(text('''
            SELECT COUNT(*) FROM fact_sales f
            LEFT JOIN dim_product p ON f.product_key = p.product_key
            WHERE p.product_key IS NULL
        ''')).scalar()
    assert orphans == 0, f"{orphans} fact rows point to a non-existent product"

def test_fact_date_keys_valid(dw_engine):
    with dw_engine.connect() as c:
        orphans = c.execute(text('''
            SELECT COUNT(*) FROM fact_sales f
            LEFT JOIN dim_date d ON f.date_key = d.date_key
            WHERE d.date_key IS NULL
        ''')).scalar()
    assert orphans == 0, f"{orphans} fact rows point to a non-existent date"
