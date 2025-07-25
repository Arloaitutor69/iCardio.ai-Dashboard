import os
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ✅ Load env vars from .env file
load_dotenv()

# ✅ Register UUID for psycopg2
psycopg2.extras.register_uuid()


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# ✅ psycopg2 raw connection (used in some endpoints)
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DATA_WAREHOUSE_POSTGRES_DB"),
        user=os.getenv("DATA_WAREHOUSE_POSTGRES_USER"),
        password=os.getenv("DATA_WAREHOUSE_POSTGRES_PASSWORD"),
        host=os.getenv("DATA_WAREHOUSE_POSTGRES_HOST"),
        port=os.getenv("DATA_WAREHOUSE_POSTGRES_PORT"),
    )
