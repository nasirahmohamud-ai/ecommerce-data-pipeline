
import pandas as pd

from unittest.mock import MagicMock

from src.load_data import (
    load_customers,
    load_products,
    load_orders
)


def test_load_customers():
    cursor = MagicMock()

    customers = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "first_name": ["John", "Sarah"],
        "last_name": ["Smith", "Jones"],
        "email": ["john@email.com", "sarah@email.com"],
        "city": ["Cape Town", "George"]
    })

    result = load_customers(cursor, customers)

    assert result == 2
    cursor.executemany.assert_called_once()


def test_load_products():
    cursor = MagicMock()

    products = pd.DataFrame({
        "product_id": ["P001", "P002"],
        "product_name": ["Laptop", "Phone"],
        "category": ["Electronics", "Electronics"],
        "unit_price": [10000, 5000]
    })

    result = load_products(cursor, products)

    assert result == 2
    cursor.executemany.assert_called_once()


def test_load_orders():
    cursor = MagicMock()

    orders = pd.DataFrame({
        "order_id": ["O001", "O002"],
        "customer_id": ["C001", "C002"],
        "product_id": ["P001", "P002"],
        "quantity": [1, 2],
        "order_date": [
            pd.to_datetime("2026-10-01").date(),
            pd.to_datetime("2026-10-02").date()
        ]
    })

    result = load_orders(cursor, orders)

    assert result == 2
    cursor.executemany.assert_called_once()


def test_customer_loading_supports_duplicate_updates():
    cursor = MagicMock()

    customers = pd.DataFrame({
        "customer_id": ["C001"],
        "first_name": ["John"],
        "last_name": ["Smith"],
        "email": ["john@email.com"],
        "city": ["Cape Town"]
    })

    load_customers(cursor, customers)

    sql = cursor.executemany.call_args[0][0]

    assert "ON DUPLICATE KEY UPDATE" in sql

def test_customer_loading_supports_duplicate_updates():
    cursor = MagicMock()

    customers = pd.DataFrame({
        "customer_id": ["C001"],
        "first_name": ["John"],
        "last_name": ["Smith"],
        "email": ["john@email.com"],
        "city": ["Cape Town"]
    })

    load_customers(cursor, customers)

    sql = cursor.executemany.call_args[0][0]

    assert "ON DUPLICATE KEY UPDATE" in sql