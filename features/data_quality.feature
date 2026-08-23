Feature: Data Quality Validation

  Scenario: Sales totals are calculated correctly
    Given the ETL pipeline has run
    Then every sale total should equal quantity multiplied by unit price

  Scenario: No orphaned records exist in the warehouse
    Given the ETL pipeline has run
    Then every fact record should reference a valid product
    And every fact record should reference a valid customer
