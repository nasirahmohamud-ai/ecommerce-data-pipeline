import sys
from pathlib import Path

import pandas as pd


# 1. Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Locate the cleaned orders file
ORDERS_FILE = BASE_DIR / "data" / "processed" / "clean_orders.csv"

# 3. Load cleaned orders
orders = pd.read_csv(ORDERS_FILE)

print("\nDATA VALIDATION REPORT")
print("----------------------")

# 4. Check for missing values
missing_values = orders.isnull().sum().sum()

print("Missing values:", missing_values)

# 5. Check for duplicate order IDs
duplicate_ids = orders["order_id"].duplicated().sum()

print("Duplicate order IDs:", duplicate_ids)

# 6. Check for invalid quantities
invalid_quantities = (orders["quantity"] <= 0).sum()

print("Invalid quantities:", invalid_quantities)

# 7. Check for missing order dates
missing_dates = orders["order_date"].isnull().sum()

print("Missing order dates:", missing_dates)

# 8. Decide whether validation passed
if (
    missing_values > 0
    or duplicate_ids > 0
    or invalid_quantities > 0
    or missing_dates > 0
):
    print("\nVALIDATION FAILED!")
    sys.exit(1)

print("\nVALIDATION PASSED!")