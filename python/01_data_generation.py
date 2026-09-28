import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# SUPPLY CHAIN DATA GENERATION

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_PATH, exist_ok=True)

print("=" * 60)
print("SUPPLY CHAIN DATA GENERATION STARTED")
print("=" * 60)

# 1. SUPPLIERS

supplier_count = 25

suppliers = pd.DataFrame({
    "Supplier_ID": [f"S{i:03d}" for i in range(1, supplier_count + 1)],
    "Supplier_Name": [f"Supplier {chr(64 + i)}" for i in range(1, supplier_count + 1)],
    "Region": np.random.choice(
        ["Maharashtra", "Gujarat", "Karnataka", "Tamil Nadu", "Delhi"],
        supplier_count
    ),
    "Lead_Time_Days": np.random.randint(3, 15, supplier_count),
    "Supplier_Rating": np.round(
        np.random.uniform(3.0, 5.0, supplier_count), 1
    ),
    "Defect_Rate": np.round(
        np.random.uniform(0.5, 6.0, supplier_count), 2
    )
})

suppliers.to_csv(
    f"{RAW_PATH}/suppliers.csv",
    index=False
)

print(f"Suppliers created: {len(suppliers):,}")


# 2. PRODUCTS

product_count = 100

categories = [
    "Electronics",
    "Home Appliances",
    "Furniture",
    "Office Supplies",
    "Accessories"
]

products = pd.DataFrame({
    "Product_ID": [f"P{i:04d}" for i in range(1, product_count + 1)],
    "Product_Name": [f"Product {i:03d}" for i in range(1, product_count + 1)],
    "Category": np.random.choice(
        categories,
        product_count
    ),
    "Unit_Cost": np.round(
        np.random.uniform(200, 5000, product_count),
        2
    )
})

products["Selling_Price"] = np.round(
    products["Unit_Cost"] *
    np.random.uniform(1.15, 1.60, product_count),
    2
)

products.to_csv(
    f"{RAW_PATH}/products.csv",
    index=False
)

print(f"Products created: {len(products):,}")


# 3. WAREHOUSES

warehouse_count = 8

warehouses = pd.DataFrame({
    "Warehouse_ID": [f"W{i:03d}" for i in range(1, warehouse_count + 1)],
    "Warehouse_Name": [
        "Mumbai Central",
        "Pune Distribution",
        "Bangalore Hub",
        "Delhi North",
        "Ahmedabad Hub",
        "Chennai South",
        "Hyderabad Hub",
        "Kolkata East"
    ],
    "City": [
        "Mumbai",
        "Pune",
        "Bangalore",
        "Delhi",
        "Ahmedabad",
        "Chennai",
        "Hyderabad",
        "Kolkata"
    ],
    "Capacity": np.random.randint(
        5000,
        20000,
        warehouse_count
    )
})

warehouses.to_csv(
    f"{RAW_PATH}/warehouses.csv",
    index=False
)

print(f"Warehouses created: {len(warehouses):,}")


# 4. CUSTOMERS

customer_count = 2000

customers = pd.DataFrame({
    "Customer_ID": [
        f"C{i:05d}" for i in range(1, customer_count + 1)
    ],
    "Customer_Name": [
        f"Customer {i:04d}" for i in range(1, customer_count + 1)
    ],
    "Region": np.random.choice(
        ["North", "South", "East", "West", "Central"],
        customer_count
    ),
    "Customer_Segment": np.random.choice(
        ["Consumer", "Small Business", "Enterprise"],
        customer_count,
        p=[0.55, 0.30, 0.15]
    )
})

customers.to_csv(
    f"{RAW_PATH}/customers.csv",
    index=False
)

print(f"Customers created: {len(customers):,}")


# DATE RANGE

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

date_range = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

# 5. PURCHASE ORDERS

po_count = 10000

po_dates = np.random.choice(
    date_range,
    po_count
)

purchase_orders = pd.DataFrame({
    "PO_ID": [f"PO{i:06d}" for i in range(1, po_count + 1)],
    "Supplier_ID": np.random.choice(
        suppliers["Supplier_ID"],
        po_count
    ),
    "Product_ID": np.random.choice(
        products["Product_ID"],
        po_count
    ),
    "Warehouse_ID": np.random.choice(
        warehouses["Warehouse_ID"],
        po_count
    ),
    "Order_Date": po_dates,
    "Quantity": np.random.randint(
        20,
        1000,
        po_count
    )
})

# Expected delivery
supplier_lookup = suppliers.set_index(
    "Supplier_ID"
)["Lead_Time_Days"]

purchase_orders["Lead_Time_Days"] = (
    purchase_orders["Supplier_ID"]
    .map(supplier_lookup)
)

purchase_orders["Expected_Date"] = (
    pd.to_datetime(purchase_orders["Order_Date"])
    + pd.to_timedelta(
        purchase_orders["Lead_Time_Days"],
        unit="D"
    )
)

# Actual delivery with some delays
delay = np.random.choice(
    [0, 1, 2, 3, 5, 7],
    po_count,
    p=[0.65, 0.10, 0.08, 0.07, 0.06, 0.04]
)

purchase_orders["Received_Date"] = (
    purchase_orders["Expected_Date"]
    + pd.to_timedelta(delay, unit="D")
)

purchase_orders.drop(
    columns=["Lead_Time_Days"],
    inplace=True
)

purchase_orders.to_csv(
    f"{RAW_PATH}/purchase_orders.csv",
    index=False
)

print(f"Purchase orders created: {len(purchase_orders):,}")


# 6. CUSTOMER ORDERS

order_count = 30000

order_dates = np.random.choice(
    date_range,
    order_count
)

orders = pd.DataFrame({
    "Order_ID": [
        f"O{i:07d}" for i in range(1, order_count + 1)
    ],
    "Customer_ID": np.random.choice(
        customers["Customer_ID"],
        order_count
    ),
    "Product_ID": np.random.choice(
        products["Product_ID"],
        order_count
    ),
    "Warehouse_ID": np.random.choice(
        warehouses["Warehouse_ID"],
        order_count
    ),
    "Order_Date": order_dates,
    "Quantity": np.random.randint(
        1,
        20,
        order_count
    )
})

# Product price lookup
price_lookup = products.set_index(
    "Product_ID"
)["Selling_Price"]

orders["Unit_Price"] = orders["Product_ID"].map(
    price_lookup
)

orders["Order_Value"] = np.round(
    orders["Quantity"] * orders["Unit_Price"],
    2
)

orders.to_csv(
    f"{RAW_PATH}/orders.csv",
    index=False
)

print(f"Orders created: {len(orders):,}")


# 7. ORDER STATUS

orders["Order_Status"] = np.random.choice(
    [
        "Fulfilled",
        "Pending",
        "Cancelled"
    ],
    len(orders),
    p=[0.95, 0.03, 0.02]
)

orders.to_csv(
    f"{RAW_PATH}/orders.csv",
    index=False
)

print(
    "\nOrder Status Distribution:"
)

print(
    orders["Order_Status"]
    .value_counts()
)


# 8. SHIPMENTS

fulfilled_orders = orders[
    orders["Order_Status"] == "Fulfilled"
].copy()

shipments = fulfilled_orders[
    [
        "Order_ID",
        "Order_Date"
    ]
].copy()

shipments.insert(
    0,
    "Shipment_ID",
    [
        f"SH{i:07d}"
        for i in range(1, len(shipments) + 1)
    ]
)

shipments["Ship_Date"] = (
    pd.to_datetime(shipments["Order_Date"])
    + pd.to_timedelta(
        np.random.randint(
            1,
            4,
            len(shipments)
        ),
        unit="D"
    )
)

delivery_days = np.random.choice(
    [
        1, 2, 3, 4, 5,
        6, 7, 8, 10
    ],
    len(shipments),
    p=[
        0.10,
        0.18,
        0.22,
        0.18,
        0.12,
        0.08,
        0.06,
        0.04,
        0.02
    ]
)

shipments["Expected_Delivery_Date"] = (
    shipments["Ship_Date"]
    + pd.to_timedelta(
        3,
        unit="D"
    )
)

shipments["Delivery_Date"] = (
    shipments["Ship_Date"]
    + pd.to_timedelta(
        delivery_days,
        unit="D"
    )
)

shipments["Delivery_Status"] = np.where(
    shipments["Delivery_Date"]
    <= shipments["Expected_Delivery_Date"],
    "On Time",
    "Late"
)

shipments["Carrier"] = np.random.choice(
    [
        "BlueDart",
        "Delhivery",
        "DHL",
        "FedEx",
        "Ecom Express"
    ],
    len(shipments)
)

shipments["Shipping_Cost"] = np.round(
    np.random.uniform(
        50,
        1200,
        len(shipments)
    ),
    2
)

shipments.to_csv(
    f"{RAW_PATH}/shipments.csv",
    index=False
)

print(
    f"Fulfilled orders shipped: {len(shipments):,}"
)

print(
    f"Unfulfilled orders: "
    f"{len(orders) - len(shipments):,}"
)


# 8. INVENTORY

inventory_records = []

for warehouse in warehouses["Warehouse_ID"]:

    selected_products = np.random.choice(
        products["Product_ID"],
        100,
        replace=False
    )

    for product in selected_products:

        opening_stock = np.random.randint(
            100,
            2000
        )

        received = np.random.randint(
            50,
            800
        )

        sold = np.random.randint(
            20,
            700
        )

        closing_stock = max(
            opening_stock + received - sold,
            0
        )

        inventory_records.append([
            warehouse,
            product,
            opening_stock,
            received,
            sold,
            closing_stock
        ])

inventory = pd.DataFrame(
    inventory_records,
    columns=[
        "Warehouse_ID",
        "Product_ID",
        "Opening_Stock",
        "Received",
        "Sold",
        "Closing_Stock"
    ]
)

inventory.to_csv(
    f"{RAW_PATH}/inventory.csv",
    index=False
)

print(f"Inventory records created: {len(inventory):,}")


# FINAL SUMMARY

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETED")
print("=" * 60)

print("\nFiles created:")

for file in os.listdir(RAW_PATH):
    print(" -", file)

print("\nDataset sizes:")

print(f"Suppliers       : {len(suppliers):,}")
print(f"Products        : {len(products):,}")
print(f"Warehouses      : {len(warehouses):,}")
print(f"Customers       : {len(customers):,}")
print(f"Purchase Orders : {len(purchase_orders):,}")
print(f"Orders          : {len(orders):,}")
print(f"Shipments       : {len(shipments):,}")
print(f"Inventory       : {len(inventory):,}")

print("\nSupply Chain dataset ready!")