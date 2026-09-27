# Supply Chain Analytics & Inventory Optimization

An end-to-end data analytics and business intelligence project designed to analyze supply chain operations, revenue performance, supplier reliability, logistics efficiency, warehouse performance, and inventory risk.

The project uses Python for data generation and analysis, PostgreSQL for relational data storage and SQL analytics, and Power BI for interactive business intelligence and dashboarding.

---

## 📌 Project Overview

Modern supply chains generate large amounts of operational data across orders, suppliers, warehouses, shipments, and inventory.

This project transforms that operational data into actionable analytical insights through a complete data analytics pipeline:

**Data Generation → Data Cleaning → PostgreSQL → SQL Analysis → Power BI → Business Insights**

---

## 🎯 Business Objectives

The project focuses on answering key business questions:

- How much revenue is being generated?
- What is the average order value?
- What percentage of orders are fulfilled?
- How frequently are shipments delayed?
- Which suppliers have higher on-time delivery percentages?
- What is the average supplier lead time?
- Which product categories contribute more revenue?
- Which warehouses generate more revenue?
- Where are stockout events occurring?
- What is the overall inventory turnover?
- How does revenue change month by month?
- What are the major supply chain operational patterns?

---

## 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Data Visualization | Matplotlib |
| Database | PostgreSQL |
| Query Language | SQL |
| Business Intelligence | Microsoft Power BI |
| Calculations | DAX |
| Development | VS Code |
| Version Control | Git & GitHub |

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │   Data Generation   │
                    │      Python         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Raw CSV Data    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Cleaning & EDA │
                    │      Python         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │      Database       │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐       ┌─────────────┐
             │ SQL Analysis│       │ Power BI    │
             │   & KPIs    │       │ Data Model  │
             └─────────────┘       └──────┬──────┘
                                          │
                                          ▼
                                  ┌───────────────┐
                                  │ DAX Measures  │
                                  └───────┬───────┘
                                          │
                                          ▼
                                  ┌───────────────┐
                                  │   Executive   │
                                  │   Dashboard   │
                                  └───────┬───────┘
                                          │
                                          ▼
                                  ┌───────────────┐
                                  │    Business   │
                                  │    Insights   │
                                  └───────────────┘