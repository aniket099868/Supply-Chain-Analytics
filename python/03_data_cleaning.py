import pandas as pd
import numpy as np
import os


# SUPPLY CHAIN DATA CLEANING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_PATH, exist_ok=True)

print("=" * 70)
print("SUPPLY CHAIN DATA CLEANING")
print("=" * 70)


### 1. SUPPLIERS ###

suppliers = pd.read_csv(
    f"{RAW_PATH}/suppliers.csv"
)

suppliers = suppliers.drop_duplicates(
    subset=["Supplier_ID"]
)

suppliers["Lead_Time_Days"] = suppliers[
    "Lead_Time_Days"
].astype(int)

suppliers["Supplier_Rating"] = suppliers[
    "Supplier_Rating"
].astype(float)

suppliers["Defect_Rate"] = suppliers[
    "Defect_Rate"
].astype(float)

suppliers.to_csv(
    f"{PROCESSED_PATH}/suppliers_clean.csv",
    index=False
)


### 2. PRODUCTS  ###

products = pd.read_csv(
    f"{RAW_PATH}/products.csv"
)

products = products.drop_duplicates(
    subset=["Product_ID"]
)

products["Unit_Cost"] = products[
    "Unit_Cost"
].astype(float)

products["Selling_Price"] = products[
    "Selling_Price"
].astype(float)

# Profit per unit
products["Profit_Per_Unit"] = (
    products["Selling_Price"]
    - products["Unit_Cost"]
)

# Profit margin
products["Profit_Margin"] = (
    products["Profit_Per_Unit"]
    / products["Selling_Price"]
) * 100

products["Profit_Margin"] = products[
    "Profit_Margin"
].round(2)

products.to_csv(
    f"{PROCESSED_PATH}/products_clean.csv",
    index=False
)


### 3. WAREHOUSES ###

warehouses = pd.read_csv(
    f"{RAW_PATH}/warehouses.csv"
)

warehouses = warehouses.drop_duplicates(
    subset=["Warehouse_ID"]
)

warehouses["Capacity"] = warehouses[
    "Capacity"
].astype(int)

warehouses.to_csv(
    f"{PROCESSED_PATH}/warehouses_clean.csv",
    index=False
)


### 4. CUSTOMER ###

customers = pd.read_csv(
    f"{RAW_PATH}/customers.csv"
)

customers = customers.drop_duplicates(
    subset=["Customer_ID"]
)

customers.to_csv(
    f"{PROCESSED_PATH}/customers_clean.csv",
    index=False
)


### 5. PURCHASE ORDERS ###

purchase_orders = pd.read_csv(
    f"{RAW_PATH}/purchase_orders.csv"
)

purchase_orders = purchase_orders.drop_duplicates(
    subset=["PO_ID"]
)

# Convert dates
purchase_orders["Order_Date"] = pd.to_datetime(
    purchase_orders["Order_Date"]
)

purchase_orders["Expected_Date"] = pd.to_datetime(
    purchase_orders["Expected_Date"]
)

purchase_orders["Received_Date"] = pd.to_datetime(
    purchase_orders["Received_Date"]
)

# Delivery duration
purchase_orders["Actual_Lead_Time_Days"] = (
    purchase_orders["Received_Date"]
    - purchase_orders["Order_Date"]
).dt.days

# Delay
purchase_orders["Delay_Days"] = (
    purchase_orders["Received_Date"]
    - purchase_orders["Expected_Date"]
).dt.days

# Supplier delivery status
purchase_orders["Delivery_Status"] = np.where(
    purchase_orders["Delay_Days"] > 0,
    "Late",
    "On Time"
)

purchase_orders.to_csv(
    f"{PROCESSED_PATH}/purchase_orders_clean.csv",
    index=False
)


### 6. ORDERS ###

orders = pd.read_csv(
    f"{RAW_PATH}/orders.csv"
)

orders = orders.drop_duplicates(
    subset=["Order_ID"]
)

orders["Order_Date"] = pd.to_datetime(
    orders["Order_Date"]
)

orders["Order_Status"] = orders[
    "Order_Status"
].astype(str)

orders["Quantity"] = orders[
    "Quantity"
].astype(int)

orders["Unit_Price"] = orders[
    "Unit_Price"
].astype(float)

orders["Order_Value"] = (
    orders["Quantity"]
    * orders["Unit_Price"]
)

orders["Order_Value"] = orders[
    "Order_Value"
].round(2)

orders["Order_Month"] = orders[
    "Order_Date"
].dt.to_period("M").astype(str)

orders.to_csv(
    f"{PROCESSED_PATH}/orders_clean.csv",
    index=False
)

### 7. SHIPMENTS ###

shipments = pd.read_csv(
    f"{RAW_PATH}/shipments.csv"
)

shipments = shipments.drop_duplicates(
    subset=["Shipment_ID"]
)

date_columns = [
    "Order_Date",
    "Ship_Date",
    "Expected_Delivery_Date",
    "Delivery_Date"
]

for column in date_columns:
    shipments[column] = pd.to_datetime(
        shipments[column]
    )

# Actual delivery duration
shipments["Delivery_Days"] = (
    shipments["Delivery_Date"]
    - shipments["Ship_Date"]
).dt.days

# Delay compared with expected delivery
shipments["Delay_Days"] = (
    shipments["Delivery_Date"]
    - shipments["Expected_Delivery_Date"]
).dt.days

# Prevent negative delay values
shipments["Delay_Days"] = shipments[
    "Delay_Days"
].clip(lower=0)

# Late flag
shipments["Late_Flag"] = np.where(
    shipments["Delay_Days"] > 0,
    1,
    0
)

# Shipping cost
shipments["Shipping_Cost"] = shipments[
    "Shipping_Cost"
].round(2)

shipments.to_csv(
    f"{PROCESSED_PATH}/shipments_clean.csv",
    index=False
)

### 8. INVENTORY  ###

inventory = pd.read_csv(
    f"{RAW_PATH}/inventory.csv"
)

# Remove duplicate warehouse-product combinations
inventory = inventory.drop_duplicates(
    subset=[
        "Warehouse_ID",
        "Product_ID"
    ]
)

# Ensure no negative values
numeric_columns = [
    "Opening_Stock",
    "Received",
    "Sold",
    "Closing_Stock"
]

for column in numeric_columns:
    inventory[column] = inventory[
        column
    ].clip(lower=0)

# Inventory stock-out flag
inventory["Stockout_Flag"] = np.where(
    inventory["Closing_Stock"] == 0,
    1,
    0
)

# Inventory turnover quantity
inventory["Inventory_Turnover"] = np.where(
    (
        inventory["Opening_Stock"]
        + inventory["Closing_Stock"]
    ) / 2 > 0,

    inventory["Sold"]
    / (
        (
            inventory["Opening_Stock"]
            + inventory["Closing_Stock"]
        ) / 2
    ),

    0
)

inventory["Inventory_Turnover"] = inventory[
    "Inventory_Turnover"
].round(2)

inventory.to_csv(
    f"{PROCESSED_PATH}/inventory_clean.csv",
    index=False
)


# FINAL SUMMARY

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)

print("\nProcessed files:")

for file in sorted(os.listdir(PROCESSED_PATH)):
    print(" -", file)

print("\nDataset sizes:")

print(
    f"Suppliers       : {len(suppliers):,}"
)

print(
    f"Products        : {len(products):,}"
)

print(
    f"Warehouses      : {len(warehouses):,}"
)

print(
    f"Customers       : {len(customers):,}"
)

print(
    f"Purchase Orders : {len(purchase_orders):,}"
)

print(
    f"Orders          : {len(orders):,}"
)

print(
    f"Shipments       : {len(shipments):,}"
)

print(
    f"Inventory       : {len(inventory):,}"
)

print("\nCleaning pipeline finished successfully.")