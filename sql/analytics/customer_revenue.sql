-- Customer Revenue Analysis
-- Purpose: Calculate the number of orders and total spending for each customer.

SELECT
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity * p.unit_price) AS total_spent
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY total_spent DESC;
