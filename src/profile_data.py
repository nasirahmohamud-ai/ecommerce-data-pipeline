
import pandas as pd

# Define the location of our raw data files
customers_file = "data/customers.csv"
products_file = "data/products.csv"
orders_file = "data/orders.csv"

# Load the CSV files into pandas DataFrames
customers = pd.read_csv(customers_file)
products = pd.read_csv(products_file)
orders = pd.read_csv(orders_file)

# Display the structure of each dataset
print("\n--- CUSTOMERS ---")
print(customers.info())

print("\n--- PRODUCTS ---")
print(products.info())

print("\n--- ORDERS ---")
print(orders.info())

# Count missing values in each dataset
print("\n--- MISSING VALUES ---")
print("Customers:\n", customers.isnull().sum())
print("Products:\n", products.isnull().sum())
print("Orders:\n", orders.isnull().sum())

# Detect duplicate order IDs
print("\n--- DUPLICATE ORDERS ---")
print(orders[orders.duplicated(subset=["order_id"], keep=False)])

# Check for invalid quantities
print("\n--- INVALID QUANTITIES ---")
print(orders[orders["quantity"] <= 0])
