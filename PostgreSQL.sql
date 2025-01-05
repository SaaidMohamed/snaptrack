CREATE TABLE users (
    user_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY UNIQUE NOT NULL,
	user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	created_at TIMESTAMP,
	updated_at TIMESTAMP,
	is_active BOOL,
	role VARCHAR(50)
);


CREATE TABLE receipts (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY UNIQUE NOT NULL,
	user_id bigint REFERENCES users(user_id) ON DELETE CASCADE,
    merchant_name VARCHAR(255),
    merchant_address TEXT,
    date DATE,
    time TIME,
    total NUMERIC(10, 2),
    currency VARCHAR(10),
    ocr_confidence NUMERIC(5, 2)
);

CREATE TABLE receipt_items (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY UNIQUE NOT NULL,
	user_id bigint REFERENCES users(user_id) ON DELETE CASCADE,
    receipt_id bigint REFERENCES receipts(id) ON DELETE CASCADE,
    description TEXT,
    amount NUMERIC(10, 2),
    qty INTEGER
);
SELECT * FROM RECEIPTS
SELECT * FROM receipt_items
