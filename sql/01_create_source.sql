CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(20),
    name VARCHAR(100),
    category VARCHAR(50),
    unit_price NUMERIC(10,2)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    order_date DATE,
    store_id INT
);
