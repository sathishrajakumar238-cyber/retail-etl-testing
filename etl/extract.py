import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

SOURCE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_source"

def extract():
    engine = create_engine(SOURCE_URL)
    customers = pd.read_sql("SELECT * FROM customers", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    orders = pd.read_sql("SELECT * FROM orders", engine)
    return customers, products, orders
