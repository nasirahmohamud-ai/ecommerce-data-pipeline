USE ecommerce_dw;

SELECT
    order_id,
    product_id,
    quantity,
    order_date,
    quantity * (
        SELECT unit_price
        FROM products
        WHERE products.product_id = orders.product_id
    ) AS total_revenue
FROM orders;

-- Calculate revenue using an INNER JOIN

SELECT
    orders.order_id,
    orders.customer_id,
    products.product_name,
    orders.quantity,
    products.unit_price,
    orders.quantity * products.unit_price AS total_revenue

FROM orders

INNER JOIN products
    ON orders.product_id = products.product_id;

    SELECT
    products.category,
    SUM(orders.quantity * products.unit_price) AS total_revenue

FROM orders

INNER JOIN products
    ON orders.product_id = products.product_id

GROUP BY products.category

ORDER BY total_revenue DESC;

SELECT
    SUM(orders.quantity * products.unit_price)
    AS total_business_revenue

FROM orders

INNER JOIN products
    ON orders.product_id = products.product_id;

    SELECT
    customers.customer_id,
    customers.first_name,
    customers.last_name,

    SUM(
        orders.quantity * products.unit_price
    ) AS total_spent

FROM orders

INNER JOIN customers
    ON orders.customer_id = customers.customer_id

INNER JOIN products
    ON orders.product_id = products.product_id

GROUP BY
    customers.customer_id,
    customers.first_name,
    customers.last_name

ORDER BY total_spent DESC;

SELECT
    COUNT(orders.order_id) AS total_orders,

    SUM(orders.quantity) AS total_units_sold,

    ROUND(
        SUM(orders.quantity * products.unit_price)
        / COUNT(orders.order_id), 2
    ) AS average_order_value

FROM orders

INNER JOIN products
    ON orders.product_id = products.product_id;