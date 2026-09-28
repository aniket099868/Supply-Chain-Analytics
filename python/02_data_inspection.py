import pandas as pd
import os

# SUPPLY CHAIN DATA INSPECTION

RAW_PATH = "../data/raw"

files = [
    "suppliers.csv",
    "products.csv",
    "warehouses.csv",
    "customers.csv",
    "purchase_orders.csv",
    "orders.csv",
    "shipments.csv",
    "inventory.csv"
]

print("=" * 70)
print("SUPPLY CHAIN DATA INSPECTION")
print("=" * 70)


for file in files:

    path = os.path.join(RAW_PATH, file)

    df = pd.read_csv(path)

    print("\n" + "=" * 70)
    print(f"FILE: {file}")
    print("=" * 70)

    # Shape
    print(f"\nRows      : {df.shape[0]:,}")
    print(f"Columns   : {df.shape[1]}")

    # Columns
    print("\nColumns:")
    print(list(df.columns))

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("No missing values found.")
    else:
        print(missing[missing > 0])

    # Duplicate rows
    duplicates = df.duplicated().sum()

    print(f"\nDuplicate Rows: {duplicates:,}")

    # Numerical summary
    numeric_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    if len(numeric_columns) > 0:

        print("\nNumerical Summary:")

        print(
            df[numeric_columns]
            .describe()
            .round(2)
        )


# ORDERS CHECK

print("\n" + "=" * 70)
print("ORDER DATA QUALITY CHECK")
print("=" * 70)

orders = pd.read_csv(
    f"{RAW_PATH}/orders.csv"
)

print(
    "\nOrders with Quantity <= 0:",
    (orders["Quantity"] <= 0).sum()
)

print(
    "Orders with Unit Price <= 0:",
    (orders["Unit_Price"] <= 0).sum()
)

print(
    "Orders with Order Value <= 0:",
    (orders["Order_Value"] <= 0).sum()
)


# SHIPMENT CHECK

print("\n" + "=" * 70)
print("SHIPMENT DATA QUALITY CHECK")
print("=" * 70)

shipments = pd.read_csv(
    f"{RAW_PATH}/shipments.csv"
)

shipments["Order_Date"] = pd.to_datetime(
    shipments["Order_Date"]
)

shipments["Ship_Date"] = pd.to_datetime(
    shipments["Ship_Date"]
)

shipments["Expected_Delivery_Date"] = pd.to_datetime(
    shipments["Expected_Delivery_Date"]
)

shipments["Delivery_Date"] = pd.to_datetime(
    shipments["Delivery_Date"]
)

print(
    "\nShipments delivered before shipping:",
    (
        shipments["Delivery_Date"]
        < shipments["Ship_Date"]
    ).sum()
)

print(
    "Shipments with delivery before expected date:",
    (
        shipments["Delivery_Date"]
        < shipments["Expected_Delivery_Date"]
    ).sum()
)

print(
    "\nDelivery Status Distribution:"
)

print(
    shipments["Delivery_Status"]
    .value_counts()
)


# INVENTORY CHECK

print("\n" + "=" * 70)
print("INVENTORY DATA QUALITY CHECK")
print("=" * 70)

inventory = pd.read_csv(
    f"{RAW_PATH}/inventory.csv"
)

print(
    "\nNegative Opening Stock:",
    (inventory["Opening_Stock"] < 0).sum()
)

print(
    "Negative Received Quantity:",
    (inventory["Received"] < 0).sum()
)

print(
    "Negative Sold Quantity:",
    (inventory["Sold"] < 0).sum()
)

print(
    "Negative Closing Stock:",
    (inventory["Closing_Stock"] < 0).sum()
)


# FINAL MESSAGE

print("\n" + "=" * 70)
print("DATA INSPECTION COMPLETED")
print("=" * 70)