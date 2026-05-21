-- Optimized BigQuery Analytics Queries
-- Uses partitioned tables for cost-efficient execution

-- 1. Revenue by region (scans only relevant partitions)
SELECT region, ROUND(SUM(total_amount), 2) AS revenue,
       COUNT(DISTINCT order_id) AS orders
FROM enterprise_analytics.fact_orders f
JOIN enterprise_analytics.dim_customers c USING(customer_id)
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'
  AND status = 'completed'
GROUP BY region ORDER BY revenue DESC;

-- 2. Monthly trend with partitioning optimization
SELECT EXTRACT(YEAR FROM order_date) AS year,
       EXTRACT(MONTH FROM order_date) AS month,
       COUNT(order_id) AS orders,
       ROUND(SUM(total_amount), 2) AS revenue
FROM enterprise_analytics.fact_orders
WHERE status = 'completed'
GROUP BY year, month ORDER BY year, month;

-- 3. Category performance (uses clustering on product_id)
SELECT p.category, COUNT(f.order_id) AS orders,
       ROUND(SUM(f.total_amount), 2) AS revenue
FROM enterprise_analytics.fact_orders f
JOIN enterprise_analytics.dim_products p USING(product_id)
WHERE f.status = 'completed'
GROUP BY p.category ORDER BY revenue DESC;
