import os
from dotenv import load_dotenv
from faker import Faker
import psycopg2
import random
from datetime import date, timedelta

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

fake = Faker()
conn = psycopg2.connect(dbname="retail_source", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cur = conn.cursor()

customer_ids = []
for _ in range(200):
    cur.execute(
        "INSERT INTO customers (name, address, city) VALUES (%s, %s, %s) RETURNING customer_id",
        (fake.name(), fake.street_address(), fake.city())
    )
    customer_ids.append(cur.fetchone()[0])

categories = ["Electronics", "Grocery", "Apparel", "Home"]
product_ids = []
for _ in range(50):
    cur.execute(
        "INSERT INTO products (sku, name, category, unit_price) VALUES (%s, %s, %s, %s) RETURNING product_id",
        (fake.bothify("SKU-####"), fake.word().capitalize(), random.choice(categories), round(random.uniform(5, 500), 2))
    )
    product_ids.append(cur.fetchone()[0])

for _ in range(2000):
    cur.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, order_date, store_id) VALUES (%s, %s, %s, %s, %s)",
        (random.choice(customer_ids), random.choice(product_ids), random.randint(1, 5),
         date.today() - timedelta(days=random.randint(0, 365)), random.randint(1, 10))
    )

conn.commit()
print("Source data generated: 200 customers, 50 products, 2000 orders")
