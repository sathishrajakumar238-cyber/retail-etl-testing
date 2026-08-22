from extract import extract
from transform import transform_and_load_customers_scd2, transform_and_load_products, transform_and_load_facts

def run():
    print("Step 1: Extracting data from source...")
    customers, products, orders = extract()
    print(f"  Extracted {len(customers)} customers, {len(products)} products, {len(orders)} orders")

    print("Step 2: Loading customer dimension (SCD2)...")
    transform_and_load_customers_scd2(customers)

    print("Step 3: Loading product dimension...")
    transform_and_load_products(products)

    print("Step 4: Loading fact table...")
    transform_and_load_facts(orders)

    print("ETL run complete.")

if __name__ == "__main__":
    run()