Feature: SCD Type 2 Customer History Tracking

  Scenario: Customer address change creates historical record
    Given customer 1 has a current address on file
    When the customer address is updated in the source system
    And the ETL pipeline runs
    Then the previous address record should be marked as not current
    And a new current record should exist with the updated address

  Scenario: Only one current record exists per customer
    Given the ETL pipeline has run
    Then each customer should have exactly one current record in the warehouse
