# Supply Chain Analytics & Inventory Optimization
## Business Insights Report

---

## 1. Executive Summary

This project analyzes a simulated supply chain covering suppliers, products,
customers, warehouses, purchase orders, customer orders, shipments, and
inventory.

The analysis combines Python, PostgreSQL, SQL analytics, and Power BI to
evaluate revenue performance, fulfillment, delivery reliability, supplier
performance, warehouse operations, and inventory efficiency.

---

## 2. Key Business KPIs

| KPI | Result |
|---|---:|
| Total Orders | 30,000 |
| Total Units Ordered | 299,998 |
| Total Revenue | ₹1,122,511,632.96 |
| Average Order Value | ₹37,417.05 |
| Fulfilled Orders | 28,569 |
| Pending Orders | 851 |
| Cancelled Orders | 580 |
| Fulfillment Rate | 95.23% |
| Total Shipments | 28,569 |
| On-Time Shipments | 14,295 |
| Late Shipments | 14,274 |
| Late Delivery Rate | 49.96% |
| Average Delivery Time | 3.85 days |
| Average Delay | 1.23 days |
| Total Shipping Cost | ₹17,914,216.39 |
| Average Shipping Cost | ₹627.05 |
| Stockout Events | 19 |
| Average Inventory Turnover | 0.63x |

---

## 3. Order Performance

The dataset contains 30,000 customer orders with a total ordered quantity
of 299,998 units.

The total order value is approximately ₹1.12 billion, with an average
order value of approximately ₹37,417.

Order status distribution:

| Status | Orders | Percentage |
|---|---:|---:|
| Fulfilled | 28,569 | 95.23% |
| Pending | 851 | 2.84% |
| Cancelled | 580 | 1.93% |

The majority of orders are fulfilled, while a smaller portion remains
pending or cancelled.

---

## 4. Delivery Performance

There are 28,569 shipments corresponding to fulfilled orders.

| Metric | Result |
|---|---:|
| Total Shipments | 28,569 |
| On-Time Shipments | 14,295 |
| Late Shipments | 14,274 |
| Late Delivery Rate | 49.96% |
| Average Delivery Time | 3.85 days |
| Average Delay | 1.23 days |

The shipment analysis shows that approximately half of the shipments were
classified as late in the simulated dataset.

Carrier-level analysis was performed to compare shipment volume, late
delivery percentage, delivery time, delay, and shipping cost.

---

## 5. Supplier Performance

The analysis covers 25 suppliers.

Overall supplier statistics:

| Metric | Result |
|---|---:|
| Total Suppliers | 25 |
| Average Supplier Rating | 3.94 |
| Average Defect Rate | 3.10% |
| Average Planned Lead Time | 9.52 days |

Supplier performance was evaluated using:

- Purchase order volume
- Actual lead time
- Delay days
- On-time delivery percentage
- Supplier rating
- Defect rate

The Power BI dashboard highlights the top 10 suppliers by on-time
delivery performance.

The highest observed supplier on-time delivery percentages in the SQL
analysis were approximately in the high-60% range.

---

## 6. Inventory Performance

Inventory analysis covers 800 warehouse-product combinations.

| Metric | Result |
|---|---:|
| Opening Stock | 824,416 |
| Stock Received | 338,098 |
| Stock Sold | 288,059 |
| Closing Stock | 877,594 |
| Stockout Events | 19 |
| Average Inventory Turnover | 0.63x |

Inventory turnover and stockout events were analyzed at warehouse and
product levels.

Stockout events identified by warehouse include:

| Warehouse | Stockout Events |
|---|---:|
| W002 | 6 |
| W007 | 3 |
| W001 | 2 |
| W003 | 2 |
| W004 | 2 |
| W005 | 2 |
| W006 | 1 |
| W008 | 1 |

---

## 7. Revenue Trend

Monthly revenue was analyzed for the full 2025 period.

Monthly order volume ranged from approximately 2,288 to 2,650 orders.

The Power BI dashboard provides a monthly revenue trend from January
through December 2025, allowing users to identify changes in revenue
across the year.

---

## 8. Product Category Performance

Revenue was analyzed across product categories using the product and order
tables.

The Power BI dashboard compares category-level revenue and identifies
differences in contribution between categories.

The analysis also includes:

- Units sold
- Revenue
- Unit cost
- Selling price
- Profit per unit
- Profit margin

---

## 9. Warehouse Performance

Warehouse-level analysis combines order revenue with inventory and
stockout information.

The dashboard compares:

- Warehouse revenue
- Units sold
- Stockout events
- Inventory turnover

This provides a consolidated view of commercial activity and inventory
risk across warehouse locations.

---

## 10. Business Analysis Areas

The project provides analytical coverage across four major areas:

### Revenue Intelligence

- Revenue by month
- Revenue by product category
- Average order value
- Order volume
- Product profitability

### Supplier Intelligence

- Supplier rating
- Defect rate
- Planned lead time
- Actual lead time
- Purchase-order delays
- On-time delivery percentage

### Logistics Intelligence

- Shipment volume
- On-time shipments
- Late shipments
- Delivery time
- Delay days
- Carrier performance
- Shipping cost

### Inventory Intelligence

- Opening inventory
- Stock received
- Units sold
- Closing inventory
- Stockout events
- Inventory turnover
- Warehouse-level inventory risk

---

## 11. Technology Stack

### Data Generation & Analysis
- Python
- Pandas
- NumPy
- Matplotlib

### Database
- PostgreSQL
- SQL

### Business Intelligence
- Microsoft Power BI
- DAX

### Development
- Visual Studio Code
- Git
- GitHub

---

## 12. Project Architecture

```text
Data Generation
      ↓
Raw CSV Data
      ↓
Data Cleaning & Validation
      ↓
Processed CSV Data
      ↓
PostgreSQL Database
      ↓
SQL Business Analysis
      ↓
Power BI Data Model
      ↓
DAX Measures
      ↓
Executive Dashboard
      ↓
Business Insights