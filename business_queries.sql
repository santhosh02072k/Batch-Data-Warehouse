-- ============================================================
-- Business Analytics Queries for E-Commerce Data Warehouse
-- Run via Presto/Trino for fast interactive SQL
-- ============================================================

-- 1. Daily revenue by region (last 30 days)
SELECT
    d.date,
    c.region,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.total_amount), 2) AS revenue
FROM ecommerce_dw.fact_orders f
JOIN ecommerce_dw.dim_customers c ON f.customer_id = c.customer_id
JOIN ecommerce_dw.dim_dates d ON f.date_id = d.date_id
WHERE f.status = 'completed'
GROUP BY d.date, c.region
ORDER BY d.date DESC, revenue DESC;

-- 2. Top 10 selling products by revenue
SELECT
    p.name AS product_name,
    p.category,
    COUNT(f.order_id) AS orders,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.total_amount), 2) AS total_revenue
FROM ecommerce_dw.fact_orders f
JOIN ecommerce_dw.dim_products p ON f.product_id = p.product_id
WHERE f.status = 'completed'
GROUP BY p.name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. Monthly revenue trend
SELECT
    f.order_year,
    f.order_month,
    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(DISTINCT f.customer_id) AS unique_customers,
    ROUND(SUM(f.total_amount), 2) AS monthly_revenue,
    ROUND(AVG(f.total_amount), 2) AS avg_order_value
FROM ecommerce_dw.fact_orders f
WHERE f.status = 'completed'
GROUP BY f.order_year, f.order_month
ORDER BY f.order_year, f.order_month;

-- 4. Customer retention: repeat buyers
SELECT
    repeat_orders,
    COUNT(*) AS customer_count
FROM (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS repeat_orders
    FROM ecommerce_dw.fact_orders
    WHERE status = 'completed'
    GROUP BY customer_id
) sub
GROUP BY repeat_orders
ORDER BY repeat_orders;

-- 5. Revenue by product category
SELECT
    p.category,
    COUNT(f.order_id) AS total_orders,
    ROUND(SUM(f.total_amount), 2) AS category_revenue,
    ROUND(AVG(f.total_amount), 2) AS avg_order_value
FROM ecommerce_dw.fact_orders f
JOIN ecommerce_dw.dim_products p ON f.product_id = p.product_id
WHERE f.status = 'completed'
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 6. Regional growth analysis (quarter over quarter)
SELECT
    c.region,
    d.quarter,
    d.year,
    ROUND(SUM(f.total_amount), 2) AS quarterly_revenue,
    COUNT(DISTINCT f.customer_id) AS unique_customers
FROM ecommerce_dw.fact_orders f
JOIN ecommerce_dw.dim_customers c ON f.customer_id = c.customer_id
JOIN ecommerce_dw.dim_dates d ON f.date_id = d.date_id
WHERE f.status = 'completed'
GROUP BY c.region, d.quarter, d.year
ORDER BY c.region, d.year, d.quarter;
