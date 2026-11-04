
-- =========================================
-- E-COMMERCE DATA WAREHOUSE
-- =========================================

CREATE DATABASE IF NOT EXISTS ecommerce_warehouse;

USE ecommerce_warehouse;


-- =========================================
-- 1. CUSTOMER DIMENSION
-- =========================================

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    city VARCHAR(100)
) ENGINE=InnoDB;


-- =========================================
-- 2. PRODUCT DIMENSION
-- =========================================

CREATE TABLE IF NOT EXISTS dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(10) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL
) ENGINE=InnoDB;


-- =========================================
-- 3. DATE DIMENSION
-- =========================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_number INT NOT NULL,
    month_number INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INT NOT NULL,
    year_number INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL
) ENGINE=InnoDB;


-- =========================================
-- 4. SALES FACT TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(10) NOT NULL,

    CONSTRAINT uq_fact_sales_order UNIQUE (order_id),

    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    date_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    sales_amount DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),

    CONSTRAINT fk_sales_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT chk_sales_quantity
        CHECK (quantity > 0)
) ENGINE=InnoDB;
