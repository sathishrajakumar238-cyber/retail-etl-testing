# Test Plan - Traceability Matrix

Maps each requirement to its automated test, ensuring full coverage of the ETL pipeline.

| Test ID | Requirement | Category | Test File / Function | Status |
|---|---|---|---|---|
| TC-001 | Order count in source must match fact table | Reconciliation | test_reconciliation.py::test_row_count_orders_vs_fact | Pass |
| TC-002 | Total quantity sold must match between source and warehouse | Reconciliation | test_reconciliation.py::test_revenue_reconciliation | Pass |
| TC-003 | Every fact row must reference a valid customer | Reconciliation | test_reconciliation.py::test_no_orphaned_fact_customers | Pass |
| TC-004 | Every fact row must reference a valid product | Referential Integrity | test_referential_integrity.py::test_fact_product_keys_valid | Pass |
| TC-005 | Every fact row must reference a valid date | Referential Integrity | test_referential_integrity.py::test_fact_date_keys_valid | Pass |
| TC-006 | Only one current record per customer at any time | SCD Type 2 | test_scd2.py::test_only_one_current_row_per_customer | Pass |
| TC-007 | Expired customer records must have an end date | SCD Type 2 | test_scd2.py::test_expired_rows_have_end_date | Pass |
| TC-008 | Customer address changes must preserve history | SCD Type 2 | test_scd2.py::test_history_preserved_after_change | Pass |
| TC-009 | total_amount must equal quantity times unit_price | Transformation Logic | test_transformation.py::test_total_amount_calculation | Pass |
| TC-010 | No sale can have zero or negative quantity | Transformation Logic | test_transformation.py::test_no_negative_or_zero_quantities | Pass |
| TC-011 | No product can have a null price | Transformation Logic | test_transformation.py::test_no_null_prices_in_products | Pass |
| TC-012 | No duplicate products should exist in dim_product | Transformation Logic | test_transformation.py::test_no_duplicate_products | Pass |

## BDD Scenarios

| Scenario ID | Description | Feature File | Status |
|---|---|---|---|
| BDD-001 | Order counts match between source and warehouse after ETL run | features/reconciliation.feature | Pass |

## Known Issues Found and Resolved

| Issue | Root Cause | Resolution |
|---|---|---|
| fact_sales row count inflating on repeated ETL runs | Missing TRUNCATE before reload | Added TRUNCATE fact_sales at start of transform_and_load_facts |
| dim_product duplicating on every ETL run | No unique constraint on product_id | Added UNIQUE constraint on dim_product.product_id |
| CI pipeline failing on SCD2 test | Fresh CI database had no prior customer state to compare against | Added a step to simulate an address change and re-run ETL before tests |
| dim_product not reflecting source updates | ON CONFLICT DO NOTHING skips existing rows entirely, never updates them | Identified as a design limitation; documented for future improvement (add UPSERT logic) |
