import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import date, timedelta

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

DW_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_dw"

engine = create_engine(DW_URL)

start_date = date(2024, 1, 1)
end_date = date(2027, 12, 31)

current = start_date
rows = []
while current <= end_date:
    date_key = int(current.strftime("%Y%m%d"))
    rows.append({
        "date_key": date_key,
        "full_date": current,
        "day": current.day,
        "month": current.month,
        "year": current.year,
        "quarter": (current.month - 1) // 3 + 1
    })
    current += timedelta(days=1)

with engine.begin() as conn:
    conn.execute(text("""
        INSERT INTO dim_date (date_key, full_date, day, month, year, quarter)
        VALUES (:date_key, :full_date, :day, :month, :year, :quarter)
        ON CONFLICT (date_key) DO NOTHING
    """), rows)

print(f"dim_date populated with {len(rows)} dates ({start_date} to {end_date})")
