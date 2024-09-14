ALTER USER delivery_user WITH REPLICATION SUPERUSER;

CREATE TABLE public.customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(15),
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store product details
CREATE TABLE public.products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    weight DECIMAL(10, 3) DEFAULT 0.0,  -- in kg
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store order details
CREATE TABLE public.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',  -- e.g. pending, shipped, delivered
    shipping_address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Table to store ordered products
CREATE TABLE public.order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Table to store shipment details
CREATE TABLE public.shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    tracking_number VARCHAR(100) UNIQUE NOT NULL,
    carrier VARCHAR(100) NOT NULL,  -- e.g., FedEx, UPS, DHL
    shipment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_delivery_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'in transit'  -- e.g., in transit, delivered
);

-- Table to store tracking events
CREATE TABLE public.tracking_events (
    tracking_event_id SERIAL PRIMARY KEY,
    shipment_id INT REFERENCES shipments(shipment_id),
    event_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255) NOT NULL,
    event_description TEXT NOT NULL
);