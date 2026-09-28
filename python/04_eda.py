import pandas as pd
import numpy as np

# SUPPLY CHAIN EDA & KPI ANALYSIS

PATH = "../data/processed"

print("=" * 70)
print("SUPPLY CHAIN EDA & KPI ANALYSIS")
print("=" * 70)

# LOAD DATA

orders = pd.read_csv(
    f"{PATH}/orders_clean.csv"
)

shipments = pd.read_csv(
    f"{PATH}/shipments_clean.csv"
)

purchase_orders = pd.read_csv(
    f"{PATH}/purchase_orders_clean.csv"
)

inventory = pd.read_csv(
    f"{PATH}/inventory_clean.csv"
)

suppliers = pd.read_csv(
    f"{PATH}/suppliers_clean.csv"
)

products = pd.read_csv(
    f"{PATH}/products_clean.csv"
)


# DATE CONVERSION

orders["Order_Date"] = pd.to_datetime(
    orders["Order_Date"]
)

shipments["Ship_Date"] = pd.to_datetime(
    shipments["Ship_Date"]
)

shipments["Delivery_Date"] = pd.to_datetime(
    shipments["Delivery_Date"]
)

purchase_orders["Order_Date"] = pd.to_datetime(
    purchase_orders["Order_Date"]
)

purchase_orders["Received_Date"] = pd.to_datetime(
    purchase_orders["Received_Date"]
)


# 1. ORDER KPIs

print("\n" + "=" * 70)
print("1. ORDER KPIs")
print("=" * 70)

total_orders = orders["Order_ID"].nunique()

total_quantity = orders["Quantity"].sum()

total_order_value = orders["Order_Value"].sum()

average_order_value = orders["Order_Value"].mean()

print(f"Total Orders        : {total_orders:,}")
print(f"Total Quantity      : {total_quantity:,}")
print(f"Total Order Value   : ₹{total_order_value:,.2f}")
print(f"Average Order Value : ₹{average_order_value:,.2f}")


# 2. DELIVERY KPIs

print("\n" + "=" * 70)
print("2. DELIVERY KPIs")
print("=" * 70)

total_shipments = shipments["Shipment_ID"].nunique()

on_time_shipments = (
    shipments["Late_Flag"] == 0
).sum()

late_shipments = (
    shipments["Late_Flag"] == 1
).sum()

late_delivery_percentage = (
    late_shipments / total_shipments
) * 100

average_delivery_days = (
    shipments["Delivery_Days"].mean()
)

average_delay_days = (
    shipments["Delay_Days"].mean()
)

print(f"Total Shipments          : {total_shipments:,}")
print(f"On-Time Shipments        : {on_time_shipments:,}")
print(f"Late Shipments           : {late_shipments:,}")
print(f"Late Delivery %          : {late_delivery_percentage:.2f}%")
print(f"Average Delivery Time    : {average_delivery_days:.2f} days")
print(f"Average Delay            : {average_delay_days:.2f} days")


# 2. FULFILLMENT KPIs

print("\n" + "=" * 70)
print("2. FULFILLMENT KPIs")
print("=" * 70)

total_orders = orders["Order_ID"].nunique()

fulfilled_orders = (
    orders["Order_Status"] == "Fulfilled"
).sum()

pending_orders = (
    orders["Order_Status"] == "Pending"
).sum()

cancelled_orders = (
    orders["Order_Status"] == "Cancelled"
).sum()

fulfillment_rate = (
    fulfilled_orders / total_orders
) * 100

pending_rate = (
    pending_orders / total_orders
) * 100

cancellation_rate = (
    cancelled_orders / total_orders
) * 100

print(f"Total Orders       : {total_orders:,}")
print(f"Fulfilled Orders   : {fulfilled_orders:,}")
print(f"Pending Orders     : {pending_orders:,}")
print(f"Cancelled Orders   : {cancelled_orders:,}")
print(f"Fulfillment Rate   : {fulfillment_rate:.2f}%")
print(f"Pending Rate       : {pending_rate:.2f}%")
print(f"Cancellation Rate  : {cancellation_rate:.2f}%")

# 3. SHIPPING COST KPIs

print("\n" + "=" * 70)
print("3. SHIPPING COST KPIs")
print("=" * 70)

total_shipping_cost = (
    shipments["Shipping_Cost"].sum()
)

average_shipping_cost = (
    shipments["Shipping_Cost"].mean()
)

print(
    f"Total Shipping Cost   : ₹{total_shipping_cost:,.2f}"
)

print(
    f"Average Shipping Cost : ₹{average_shipping_cost:,.2f}"
)


# 4. CARRIER PERFORMANCE

print("\n" + "=" * 70)
print("4. CARRIER PERFORMANCE")
print("=" * 70)

carrier_analysis = (
    shipments
    .groupby("Carrier")
    .agg(
        Shipments=("Shipment_ID", "count"),
        Average_Delivery_Days=("Delivery_Days", "mean"),
        Late_Shipments=("Late_Flag", "sum"),
        Shipping_Cost=("Shipping_Cost", "sum")
    )
)

carrier_analysis["Late_Delivery_%"] = (
    carrier_analysis["Late_Shipments"]
    / carrier_analysis["Shipments"]
) * 100

carrier_analysis = carrier_analysis.round(2)

print(
    carrier_analysis
    .sort_values(
        "Late_Delivery_%",
        ascending=False
    )
)


# 5. SUPPLIER PERFORMANCE

print("\n" + "=" * 70)
print("5. SUPPLIER PERFORMANCE")
print("=" * 70)

supplier_analysis = (
    purchase_orders
    .groupby("Supplier_ID")
    .agg(
        Purchase_Orders=("PO_ID", "count"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Lead_Time=("Actual_Lead_Time_Days", "mean"),
        Avg_Delay=("Delay_Days", "mean"),
        Late_Orders=(
            "Delivery_Status",
            lambda x: (x == "Late").sum()
        )
    )
)

supplier_analysis["On_Time_%"] = (
    1
    - (
        supplier_analysis["Late_Orders"]
        / supplier_analysis["Purchase_Orders"]
    )
) * 100

supplier_analysis = (
    supplier_analysis
    .merge(
        suppliers[
            [
                "Supplier_ID",
                "Supplier_Name",
                "Supplier_Rating",
                "Defect_Rate"
            ]
        ],
        on="Supplier_ID"
    )
)

supplier_analysis = supplier_analysis.round(2)

print(
    supplier_analysis
    .sort_values(
        "On_Time_%",
        ascending=False
    )
    .to_string(index=False)
)


# 6. INVENTORY KPIs

print("\n" + "=" * 70)
print("6. INVENTORY KPIs")
print("=" * 70)

total_opening_stock = (
    inventory["Opening_Stock"].sum()
)

total_received = (
    inventory["Received"].sum()
)

total_sold = (
    inventory["Sold"].sum()
)

total_closing_stock = (
    inventory["Closing_Stock"].sum()
)

stockout_events = (
    inventory["Stockout_Flag"].sum()
)

stockout_rate = (
    stockout_events / len(inventory)
) * 100

average_inventory_turnover = (
    inventory["Inventory_Turnover"].mean()
)

print(
    f"Opening Stock             : {total_opening_stock:,}"
)

print(
    f"Stock Received            : {total_received:,}"
)

print(
    f"Stock Sold                : {total_sold:,}"
)

print(
    f"Closing Stock             : {total_closing_stock:,}"
)

print(
    f"Stock-out Events          : {stockout_events:,}"
)

print(
    f"Stock-out Rate            : {stockout_rate:.2f}%"
)

print(
    f"Average Inventory Turnover: "
    f"{average_inventory_turnover:.2f}x"
)


# 7. INVENTORY BY WAREHOUSE

print("\n" + "=" * 70)
print("7. INVENTORY BY WAREHOUSE")
print("=" * 70)

warehouse_inventory = (
    inventory
    .groupby("Warehouse_ID")
    .agg(
        Opening_Stock=("Opening_Stock", "sum"),
        Received=("Received", "sum"),
        Sold=("Sold", "sum"),
        Closing_Stock=("Closing_Stock", "sum"),
        Stockouts=("Stockout_Flag", "sum"),
        Avg_Turnover=("Inventory_Turnover", "mean")
    )
)

warehouse_inventory["Stockout_%"] = (
    warehouse_inventory["Stockouts"]
    / inventory.groupby(
        "Warehouse_ID"
    ).size()
) * 100

warehouse_inventory = warehouse_inventory.round(2)

print(
    warehouse_inventory
    .sort_values(
        "Stockout_%",
        ascending=False
    )
)

# 8. PRODUCT PERFORMANCE

print("\n" + "=" * 70)
print("8. PRODUCT PERFORMANCE")
print("=" * 70)

product_analysis = (
    orders
    .groupby("Product_ID")
    .agg(
        Orders=("Order_ID", "count"),
        Quantity_Sold=("Quantity", "sum"),
        Revenue=("Order_Value", "sum")
    )
    .reset_index()
)

product_analysis = product_analysis.merge(
    products[
        [
            "Product_ID",
            "Product_Name",
            "Category"
        ]
    ],
    on="Product_ID"
)

print("\nTop 10 Products by Revenue:")

print(
    product_analysis
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
    .to_string(index=False)
)



# 9. MONTHLY ORDER TREND

print("\n" + "=" * 70)
print("9. MONTHLY ORDER TREND")
print("=" * 70)

monthly_orders = (
    orders
    .groupby(
        orders["Order_Date"].dt.to_period("M")
    )
    .agg(
        Orders=("Order_ID", "count"),
        Quantity=("Quantity", "sum"),
        Revenue=("Order_Value", "sum")
    )
)

monthly_orders["Revenue"] = (
    monthly_orders["Revenue"]
    .round(2)
)

print(monthly_orders)


# FINAL SUMMARY

print("\n" + "=" * 70)
print("EDA COMPLETED")
print("=" * 70)

print("\nKey KPIs:")
print(f"Orders             : {total_orders:,}")
print(f"Order Value        : ₹{total_order_value:,.2f}")
print(f"Late Delivery      : {late_delivery_percentage:.2f}%")
print(f"Avg Delivery Time  : {average_delivery_days:.2f} days")
print(f"Shipping Cost      : ₹{total_shipping_cost:,.2f}")
print(f"Stock-out Rate     : {stockout_rate:.2f}%")
print(f"Inventory Turnover : {average_inventory_turnover:.2f}x")

print("\nSupply Chain EDA completed successfully.")