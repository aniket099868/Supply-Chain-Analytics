-- SUPPLY CHAIN ANALYTICS
-- BUSINESS KPI QUERIES


-- 1. Overall Business KPIs
SELECT
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_units,
    ROUND(SUM(order_value), 2) AS total_revenue,
    ROUND(AVG(order_value), 2) AS average_order_value,
    ROUND(
        100.0 * SUM(
            CASE WHEN order_status = 'Fulfilled' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS fulfillment_rate_pct
FROM orders;


-- 2. Delivery Performance
SELECT
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END)
        AS on_time_shipments,
    SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END)
        AS late_shipments,
    ROUND(
        100.0 * SUM(
            CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS late_delivery_pct,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM shipments;


-- 3. Shipping Cost
SELECT
    ROUND(SUM(shipping_cost), 2) AS total_shipping_cost,
    ROUND(AVG(shipping_cost), 2) AS average_shipping_cost
FROM shipments;


-- 4. Supplier Performance
SELECT
    s.supplier_id,
    s.supplier_name,
    s.region,
    s.supplier_rating,
    s.defect_rate,
    COUNT(po.po_id) AS purchase_orders,
    ROUND(AVG(po.actual_lead_time_days), 2)
        AS avg_actual_lead_time,
    ROUND(AVG(po.delay_days), 2)
        AS avg_delay_days,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN po.delivery_status = 'On Time'
                THEN 1 ELSE 0
            END
        ) / COUNT(po.po_id),
        2
    ) AS on_time_delivery_pct
FROM suppliers s
JOIN purchase_orders po
    ON s.supplier_id = po.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name,
    s.region,
    s.supplier_rating,
    s.defect_rate
ORDER BY on_time_delivery_pct DESC;


-- 5. Product Performance
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.unit_cost,
    p.selling_price,
    p.profit_per_unit,
    p.profit_margin,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.order_value), 2) AS revenue,
    ROUND(
        SUM(o.quantity * p.profit_per_unit),
        2
    ) AS estimated_profit
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
WHERE o.order_status = 'Fulfilled'
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.unit_cost,
    p.selling_price,
    p.profit_per_unit,
    p.profit_margin
ORDER BY revenue DESC;


-- 6. Warehouse Performance
SELECT
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.capacity,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(o.quantity), 0) AS units_sold,
    ROUND(COALESCE(SUM(o.order_value), 0), 2)
        AS revenue,
    COUNT(DISTINCT s.shipment_id) AS shipments,
    SUM(
        CASE
            WHEN s.delivery_status = 'Late'
            THEN 1 ELSE 0
        END
    ) AS late_shipments
FROM warehouses w
LEFT JOIN orders o
    ON w.warehouse_id = o.warehouse_id
LEFT JOIN shipments s
    ON o.order_id = s.order_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.capacity
ORDER BY revenue DESC;


-- 7. Inventory KPIs
SELECT
    SUM(opening_stock) AS opening_stock,
    SUM(received) AS received_stock,
    SUM(sold) AS sold_stock,
    SUM(closing_stock) AS closing_stock,
    SUM(stockout_flag) AS stockout_events,
    ROUND(AVG(inventory_turnover), 2)
        AS average_inventory_turnover
FROM inventory;


-- 8. Inventory by Warehouse
SELECT
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    SUM(i.closing_stock) AS closing_stock,
    SUM(i.stockout_flag) AS stockout_events,
    ROUND(AVG(i.inventory_turnover), 2)
        AS average_inventory_turnover
FROM warehouses w
JOIN inventory i
    ON w.warehouse_id = i.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name,
    w.city
ORDER BY stockout_events DESC;


-- 9. Customer Segment Performance
SELECT
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(o.order_id) AS orders,
    SUM(o.quantity) AS units,
    ROUND(SUM(o.order_value), 2) AS revenue,
    ROUND(AVG(o.order_value), 2) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'Fulfilled'
GROUP BY c.customer_segment
ORDER BY revenue DESC;


-- 10. Monthly Business Trend
SELECT
    order_month,
    COUNT(*) AS orders,
    SUM(quantity) AS units,
    ROUND(SUM(order_value), 2) AS revenue
FROM orders
WHERE order_status = 'Fulfilled'
GROUP BY order_month
ORDER BY order_month;