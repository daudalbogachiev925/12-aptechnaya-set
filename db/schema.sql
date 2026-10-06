CREATE TABLE pharmacies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    city TEXT
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    inn TEXT,
    phone TEXT
);

CREATE TABLE medicines (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    form TEXT,
    manufacturer TEXT,
    rx BOOLEAN DEFAULT FALSE,
    category TEXT
);

CREATE TABLE batches (
    id BIGSERIAL PRIMARY KEY,
    medicine_id BIGINT REFERENCES medicines(id),
    pharmacy_id INT REFERENCES pharmacies(id),
    supplier_id INT REFERENCES suppliers(id),
    qty INT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    purchase_price NUMERIC(10,2),
    expiry DATE NOT NULL,
    arrived DATE DEFAULT CURRENT_DATE
);

CREATE TABLE sales (
    id BIGSERIAL PRIMARY KEY,
    batch_id BIGINT REFERENCES batches(id),
    qty INT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    sold_at TIMESTAMP DEFAULT NOW(),
    seller TEXT,
    prescription TEXT
);

CREATE INDEX idx_batches_pharmacy ON batches(pharmacy_id);
CREATE INDEX idx_batches_expiry ON batches(expiry);
CREATE INDEX idx_sales_batch ON sales(batch_id);
CREATE INDEX idx_sales_sold_at ON sales(sold_at);
