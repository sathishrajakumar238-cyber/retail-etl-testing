import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_source")

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Connection successful:", result.scalar())
