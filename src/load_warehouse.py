from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import mysql.connector
import pandas as pd
import os

from pathlib import Path
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


# Database names
SOURCE_DB = "ecommerce_dw"
WAREHOUSE_DB = "ecommerce_warehouse"


def get_connection(database):

    connection = mysql.connector.connect(
        **DB_CONFIG,
        database=database
    )

    return connection

def get_engine(database):

    connection_url = URL.create(
        drivername="mysql+mysqlconnector",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=database
    )

    engine = create_engine(connection_url)

    return engine


def load_customers(source_connection, warehouse_connection):

    customers = pd.read_sql(
        "SELECT * FROM customers",
        source_connection
    )

    # Convert NaN into SQL NULL
    customers = customers.astype(object).where(
        pd.notna(customers),
        None
    )

    query = """
        INSERT INTO dim_customer (
            customer_id,
            first_name,
            last_name,
            email,
            city
        )
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            first_name = VALUES(first_name),
            last_name = VALUES(last_name),
            email = VALUES(email),
            city = VALUES(city)
    """

    records = [
        tuple(row)
        for row in customers.itertuples(index=False, name=None)
    ]

    cursor = warehouse_connection.cursor()

    try:
        cursor.executemany(query, records)
        warehouse_connection.commit()
    except Exception:
        warehouse_connection.rollback()
        raise
    finally:
        cursor.close()

    print(f"Customers loaded: {len(records)}")


def load_products(source_connection, warehouse_connection):

    products = pd.read_sql(
        """
        SELECT product_id, product_name, category
        FROM products
        """,
        source_connection
    )

    query = """
        INSERT INTO dim_product (
            product_id,
            product_name,
            category
        )
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            product_name = VALUES(product_name),
            category = VALUES(category)
    """

    records = [
        tuple(row)
        for row in products.itertuples(index=False, name=None)
    ]

    cursor = warehouse_connection.cursor()

    try:
        cursor.executemany(query, records)
        warehouse_connection.commit()
    except Exception:
        warehouse_connection.rollback()
        raise
    finally:
        cursor.close()

    print(f"Products loaded: {len(records)}")


def load_sales(source_connection, warehouse_connection):

    # Read orders and their product prices
    sales = pd.read_sql(
        """
        SELECT
            o.order_id,
            o.customer_id,
            o.product_id,
            o.quantity,
            o.order_date,
            p.unit_price
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        """,
        source_connection
    )

    # Prepare the sales records with warehouse keys
    cursor = warehouse_connection.cursor()

    records = []

    for _, row in sales.iterrows():

        # Find the customer's warehouse key
        cursor.execute(
            """
            SELECT customer_key
            FROM dim_customer
            WHERE customer_id = %s
            """,
            (row["customer_id"],)
        )

        customer_key = cursor.fetchone()[0]

        # Find the product's warehouse key
        cursor.execute(
            """
            SELECT product_key
            FROM dim_product
            WHERE product_id = %s
            """,
            (row["product_id"],)
        )

        product_key = cursor.fetchone()[0]

        # Convert the order date into YYYYMMDD
        date_key = int(row["order_date"].strftime("%Y%m%d"))

        # Calculate the sales amount
        sales_amount = float(row["quantity"]) * float(row["unit_price"])

        records.append((
            row["order_id"],
            customer_key,
            product_key,
            date_key,
            int(row["quantity"]),
            float(row["unit_price"]),
            sales_amount
        ))

    query = """
        INSERT INTO fact_sales (
            order_id,
            customer_key,
            product_key,
            date_key,
            quantity,
            unit_price,
            sales_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            customer_key = VALUES(customer_key),
            product_key = VALUES(product_key),
            date_key = VALUES(date_key),
            quantity = VALUES(quantity),
            unit_price = VALUES(unit_price),
            sales_amount = VALUES(sales_amount)
    """

    try:
        cursor.executemany(query, records)
        warehouse_connection.commit()
    except Exception:
        warehouse_connection.rollback()
        raise
    finally:
        cursor.close()

    print(f"Sales loaded: {len(records)}")


if __name__ == "__main__":

    source_engine = get_engine(SOURCE_DB)
    warehouse_connection = get_connection(WAREHOUSE_DB)

    try:
        load_customers(source_engine, warehouse_connection)
        load_products(source_engine, warehouse_connection)
        load_sales(source_engine, warehouse_connection)

    finally:
        source_engine.dispose()
        warehouse_connection.close()
