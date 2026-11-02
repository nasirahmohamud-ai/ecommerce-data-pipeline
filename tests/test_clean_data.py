import pandas as pd
from pathlib import Path


# Find the project folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Locate the cleaned and rejected order files
CLEAN_FILE = BASE_DIR / "data" / "processed" / "clean_orders.csv"
REJECTED_FILE = BASE_DIR / "data" / "processed" / "rejected_orders.csv"


def test_clean_orders_file_exists():
    assert CLEAN_FILE.exists()


def test_rejected_orders_file_exists():
    assert REJECTED_FILE.exists()


def test_clean_orders_have_valid_quantities():
    orders = pd.read_csv(CLEAN_FILE)

    assert (orders["quantity"] > 0).all()


def test_clean_orders_have_unique_order_ids():
    orders = pd.read_csv(CLEAN_FILE)

    assert orders["order_id"].is_unique


def test_rejected_orders_have_reasons():
    orders = pd.read_csv(REJECTED_FILE)

    assert orders["rejection_reason"].notna().all()
    assert (orders["rejection_reason"].str.strip() != "").all()