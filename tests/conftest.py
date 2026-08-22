import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

@pytest.fixture(scope="session")
def source_engine():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_source")

@pytest.fixture(scope="session")
def dw_engine():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/retail_dw")
