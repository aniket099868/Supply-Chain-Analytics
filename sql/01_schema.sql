
-- SUPPLY CHAIN ANALYTICS DATABASE
-- PostgreSQL Schema

-- 1. SUPPLIERS
CREATE TABLE suppliers (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    category VARCHAR(100),
    lead_time_days INT,
    on_time_delivery_pct DECIMAL(5,2),
    rating DECIMAL(3,2)
);


-- 2. PRODUCTS
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    unit_price DECIMAL(12,2),
    supplier_id VARCHAR(20),

    CONSTRAINT fk_products_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);


-- 3. WAREHOUSES
CREATE TABLE warehouses (
    warehouse_id VARCHAR(20) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    capacity INT
);


-- 4. CUSTOMERS
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    customer_segment VARCHAR(50)
);


-- 5. PURCHASE ORDERS
CREATE TABLE purchase_orders (
    purchase_order_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    warehouse_id VARCHAR(20) NOT NULL,
    order_date DATE,
    expected_date DATE,
    received_date DATE,
    quantity INT,
    unit_cost DECIMAL(12,2),
    total_cost DECIMAL(14,2),
    status VARCHAR(30),

    CONSTRAINT fk_po_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id),

    CONSTRAINT fk_po_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_po_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id)
);


-- 6. ORDERS
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    warehouse_id VARCHAR(20) NOT NULL,
    order_date DATE,
    quantity INT,
    unit_price DECIMAL(12,2),
    order_value DECIMAL(14,2),
    order_month VARCHAR(20),
    order_status VARCHAR(30),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_orders_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_orders_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id)
);


-- 7. SHIPMENTS
CREATE TABLE shipments (
    shipment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    carrier VARCHAR(100),
    shipping_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    delivery_status VARCHAR(30),
    delivery_days INT,
    delay_days INT,
    shipping_cost DECIMAL(12,2),

    CONSTRAINT fk_shipments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- 8. INVENTORY
CREATE TABLE inventory (
    warehouse_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    opening_stock INT,
    stock_received INT,
    stock_sold INT,
    closing_stock INT,
    reorder_level INT,
    stock_out BOOLEAN,

    PRIMARY KEY (warehouse_id, product_id),

    CONSTRAINT fk_inventory_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);