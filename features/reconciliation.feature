Feature: ETL Source to Target Reconciliation

  Scenario: Order counts match between source and warehouse
    Given the source orders table has 2000 records
    When the ETL pipeline runs
    Then the fact_sales table should have 2000 records
