
import pandas as pd

from unittest.mock import MagicMock

from src.load_warehouse import (
    load_customers,
    load_products,
    load_sales
)


def test_warehouse_loads_customers(monkeypatch):

    source_connection = MagicMock()
    warehouse_connection = MagicMock()
    cursor = MagicMock()

    warehouse_connection.cursor.return_value = cursor

    customers = pd.DataFrame({
        "customer_id": ["C001"],
        "first_name": ["Amina"],
        "last_name": ["Khan"],
        "email": ["amina@example.com"],
        "city": ["Cape Town"]
    })

    monkeypatch.setattr(
        "src.load_warehouse.pd.read_sql",
        lambda query, connection: customers
    )

    load_customers(source_connection, warehouse_connection)

    cursor.executemany.assert_called_once()
    warehouse_connection.commit.assert_called_once()


def test_warehouse_converts_missing_emails_to_null(monkeypatch):

    source_connection = MagicMock()
    warehouse_connection = MagicMock()
    cursor = MagicMock()

    warehouse_connection.cursor.return_value = cursor

    customers = pd.DataFrame({
        "customer_id": ["C005"],
        "first_name": ["Sarah"],
        "last_name": ["Jacobs"],
        "email": [None],
        "city": ["Cape Town"]
    })

    monkeypatch.setattr(
        "src.load_warehouse.pd.read_sql",
        lambda query, connection: customers
    )

    load_customers(source_connection, warehouse_connection)

    records = cursor.executemany.call_args[0][1]

    assert records[0][3] is None


def test_warehouse_loads_products(monkeypatch):

    source_connection = MagicMock()
    warehouse_connection = MagicMock()
    cursor = MagicMock()

    warehouse_connection.cursor.return_value = cursor

    products = pd.DataFrame({
        "product_id": ["P001"],
        "product_name": ["Wireless Mouse"],
        "category": ["Electronics"]
    })

    monkeypatch.setattr(
        "src.load_warehouse.pd.read_sql",
        lambda query, connection: products
    )

    load_products(source_connection, warehouse_connection)

    cursor.executemany.assert_called_once()
    warehouse_connection.commit.assert_called_once()


def test_warehouse_calculates_sales_amount(monkeypatch):

    source_connection = MagicMock()
    warehouse_connection = MagicMock()
    cursor = MagicMock()

    warehouse_connection.cursor.return_value = cursor

    sales = pd.DataFrame({
        "order_id": ["O1001"],
        "customer_id": ["C001"],
        "product_id": ["P001"],
        "quantity": [2],
        "order_date": [pd.to_datetime("2026-10-01").date()],
        "unit_price": [249.99]
    })

    monkeypatch.setattr(
        "src.load_warehouse.pd.read_sql",
        lambda query, connection: sales
    )

    cursor.fetchone.side_effect = [(1,), (1,)]

    load_sales(source_connection, warehouse_connection)

    records = cursor.executemany.call_args[0][1]

    assert records[0][0] == "O1001"
    assert records[0][4] == 2
    assert records[0][6] == 499.98

    warehouse_connection.commit.assert_called_once()
