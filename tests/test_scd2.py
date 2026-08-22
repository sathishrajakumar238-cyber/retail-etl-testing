from sqlalchemy import text

def test_only_one_current_row_per_customer(dw_engine):
    with dw_engine.connect() as c:
        violations = c.execute(text('''
            SELECT customer_id, COUNT(*) FROM dim_customer
            WHERE is_current = TRUE
            GROUP BY customer_id HAVING COUNT(*) > 1
        ''')).fetchall()
    assert len(violations) == 0, f"Customers with multiple current rows: {violations}"

def test_expired_rows_have_end_date(dw_engine):
    with dw_engine.connect() as c:
        bad = c.execute(text('''
            SELECT COUNT(*) FROM dim_customer WHERE is_current = FALSE AND end_date IS NULL
        ''')).scalar()
    assert bad == 0, f"{bad} expired rows are missing an end_date"

def test_history_preserved_after_change(dw_engine):
    with dw_engine.connect() as c:
        rows = c.execute(text('''
            SELECT * FROM dim_customer WHERE customer_id = 1 ORDER BY effective_date
        ''')).fetchall()
    assert len(rows) >= 2, "Expected historical + current row after address change"
    assert rows[-1].is_current is True
    assert rows[-2].is_current is False
