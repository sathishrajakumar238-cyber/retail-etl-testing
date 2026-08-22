CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day INT, month INT, year INT, quarter INT
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT,
    sku VARCHAR(20),
    name VARCHAR(100),
    category VARCHAR(50),
    unit_price NUMERIC(10,2)
);

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(100),
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    store_id INT,
    quantity INT,
    unit_price NUMERIC(10,2),
    total_amount NUMERIC(10,2)
);
