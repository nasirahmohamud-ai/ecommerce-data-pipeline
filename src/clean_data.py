
import pandas as pd
from pathlib import Path

# Define our project folders
DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "processed"

# Create the output folder if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load the original source data
customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")

# Step 1: Remove exact duplicate rows from orders
orders = orders.drop_duplicates()

# Step 2: Identify orders with invalid quantities
invalid_quantity = orders["quantity"] <= 0

# Step 3: Identify orders with unknown customers or products
unknown_customer = ~orders["customer_id"].isin(
    customers["customer_id"]
)

unknown_product = ~orders["product_id"].isin(
    products["product_id"]
)

# Step 4: Combine all rejection conditions
rejected_mask = (
    invalid_quantity
    | unknown_customer
    | unknown_product
)

# Step 5: Separate valid orders from rejected orders
valid_orders = orders.loc[~rejected_mask].copy()
rejected_orders = orders.loc[rejected_mask].copy()

# Record why each rejected order was rejected
rejected_orders["rejection_reason"] = ""

rejected_orders.loc[
    invalid_quantity.loc[rejected_orders.index],
    "rejection_reason"
] += "Invalid quantity; "

rejected_orders.loc[
    unknown_customer.loc[rejected_orders.index],
    "rejection_reason"
] += "Unknown customer; "

rejected_orders.loc[
    unknown_product.loc[rejected_orders.index],
    "rejection_reason"
] += "Unknown product; "

# Step 6: Save the outputs without changing the raw files
valid_orders.to_csv(
    OUTPUT_DIR / "clean_orders.csv",
    index=False
)

rejected_orders.to_csv(
    OUTPUT_DIR / "rejected_orders.csv",
    index=False
)

# Step 7: Print a summary
print("DATA CLEANING SUMMARY")
print("---------------------")
print("Raw order rows:", len(pd.read_csv(DATA_DIR / "orders.csv")))
print("After exact deduplication:", len(orders))
print("Valid orders:", len(valid_orders))
print("Rejected orders:", len(rejected_orders))

print("\nRejection report:")
print(rejected_orders[["order_id", "rejection_reason"]])

print("\nCleaned orders saved to:", OUTPUT_DIR / "clean_orders.csv")
print("Rejected orders saved to:", OUTPUT_DIR / "rejected_orders.csv")
