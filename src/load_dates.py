
import mysql.connector
import os

from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load database credentials
load_dotenv(BASE_DIR / ".env")


# Database connection settings
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
}


WAREHOUSE_DB = "ecommerce_warehouse"


def get_connection():

    connection = mysql.connector.connect(
        **DB_CONFIG,
        database=WAREHOUSE_DB
    )

    return connection


def load_dates(connection):

    cursor = connection.cursor()

    # Find the earliest and latest order dates
    cursor.execute("""
        SELECT MIN(order_date), MAX(order_date)
        FROM ecommerce_dw.orders
    """)

    start_date, end_date = cursor.fetchone()

    # Prepare the SQL statement
    query = """
        INSERT INTO dim_date (
            date_key,
            full_date,
            day_number,
            month_number,
            month_name,
            quarter_number,
            year_number,
            day_name,
            is_weekend
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            full_date = VALUES(full_date)
    """

    records = []

    # Generate every date between the first and last order
    current_date = start_date

    while current_date <= end_date:

        date_key = int(current_date.strftime("%Y%m%d"))

        day_number = current_date.day
        month_number = current_date.month
        month_name = current_date.strftime("%B")
        quarter_number = (month_number - 1) // 3 + 1
        year_number = current_date.year
        day_name = current_date.strftime("%A")
        is_weekend = current_date.weekday() >= 5

        records.append((
            date_key,
            current_date,
            day_number,
            month_number,
            month_name,
            quarter_number,
            year_number,
            day_name,
            is_weekend
        ))

        current_date += timedelta(days=1)

    try:
        cursor.executemany(query, records)
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

    print(f"Dates loaded: {len(records)}")


if __name__ == "__main__":

    connection = get_connection()

    try:
        load_dates(connection)

    finally:
        connection.close()
