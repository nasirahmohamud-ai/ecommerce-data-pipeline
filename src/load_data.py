
import os
import sys
from pathlib import Path

import pandas as pd
import mysql.connector
from dotenv import load_dotenv


# 1. Find project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Load environment settings
load_dotenv(BASE_DIR / ".env")

config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "ecommerce_dw"),
}

# 3. Define data file locations
DATA_DIR = BASE_DIR / "data"

CUSTOMERS_FILE = DATA_DIR / "customers.csv"
PRODUCTS_FILE = DATA_DIR / "products.csv"
ORDERS_FILE = DATA_DIR / "processed" / "clean_orders.csv"


# 4. Load customer records
def load_customers(cursor, customers):

    sql = """
        INSERT INTO customers
        (customer_id, first_name, last_name, email, city)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            first_name = VALUES(first_name),
            last_name = VALUES(last_name),
            email = VALUES(email),
            city = VALUES(city)
    """

    data = list(
        customers[
            ["customer_id", "first_name", "last_name",
             "email", "city"]
        ].itertuples(index=False, name=None)
    )

    cursor.executemany(sql, data)

    return len(data)


# 5. Load product records
def load_products(cursor, products):

    sql = """
        INSERT INTO products
        (product_id, product_name, category, unit_price)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            product_name = VALUES(product_name),
            category = VALUES(category),
            unit_price = VALUES(unit_price)
    """

    data = list(
        products[
            ["product_id", "product_name", "category",
             "unit_price"]
        ].itertuples(index=False, name=None)
    )

    cursor.executemany(sql, data)

    return len(data)


# 6. Load order records
def load_orders(cursor, orders):

    sql = """
        INSERT INTO orders
        (order_id, customer_id, product_id, quantity, order_date)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            customer_id = VALUES(customer_id),
            product_id = VALUES(product_id),
            quantity = VALUES(quantity),
            order_date = VALUES(order_date)
    """

    data = list(
        orders[
            ["order_id", "customer_id", "product_id",
             "quantity", "order_date"]
        ].itertuples(index=False, name=None)
    )

    cursor.executemany(sql, data)

    return len(data)


# 7. Run the complete loading process
def main():

    connection = None
    cursor = None

    try:
        # Read CSV files
        customers = pd.read_csv(CUSTOMERS_FILE)
        products = pd.read_csv(PRODUCTS_FILE)
        orders = pd.read_csv(ORDERS_FILE)

        # Convert order dates
        orders["order_date"] = pd.to_datetime(
            orders["order_date"]
        ).dt.date

        # Replace missing values with None
        customers = customers.astype(object).where(
            pd.notna(customers), None
        )
        products = products.astype(object).where(
            pd.notna(products), None
        )
        orders = orders.astype(object).where(
            pd.notna(orders), None
        )

        # Connect to MySQL
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("Connected to MySQL successfully!")

        # Load all datasets
        customer_count = load_customers(cursor, customers)
        product_count = load_products(cursor, products)
        order_count = load_orders(cursor, orders)

        # Commit database changes
        connection.commit()

        print("\nData successfully loaded!")
        print("Customers processed:", customer_count)
        print("Products processed:", product_count)
        print("Orders processed:", order_count)

    except Exception as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("Data loading failed.")
        print("Error:", error)

        sys.exit(1)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")


# 8. Only execute when this file is run directly
if __name__ == "__main__":
    main()


