-- database/test_data.sql

USE cimb_credit_card;

-- Insert test customers
INSERT INTO customers (first_name, last_name, email, phone, address_line1, address_line2, city, state, postal_code, country, date_of_birth)
VALUES 
    ('Ahmad', 'Bin Abdullah', 'ahmad@example.com', '+60123456789', '123 Jalan Merdeka', 'Taman Bahagia', 'Kuala Lumpur', 'Wilayah Persekutuan', '50100', 'Malaysia', '1980-05-15'),
    ('Siti', 'Binti Rahman', 'siti@example.com', '+60198765432', '456 Jalan Harmoni', 'Apartment 3B', 'Petaling Jaya', 'Selangor', '47810', 'Malaysia', '1985-11-23'),
    ('Raj', 'Kumar', 'raj@example.com', '+60187654321', '789 Jalan Sentosa', NULL, 'Georgetown', 'Penang', '10050', 'Malaysia', '1975-03-08');

-- Insert test accounts
INSERT INTO accounts (customer_id, account_number, card_number, card_type, credit_limit, current_balance, statement_date, payment_due_date, annual_interest_rate, opening_date)
VALUES 
    (1, 'CIMB0001234567', '5196061234567890', 'MASTERCARD', 10000.00, 3500.00, 15, 10, 17.90, '2020-01-15'),
    (2, 'CIMB0007654321', '4101567890123456', 'VISA', 15000.00, 7250.00, 20, 10, 18.50, '2019-08-22'),
    (3, 'CIMB0009876543', '5196067890123456', 'MASTERCARD', 8000.00, 1200.00, 25, 15, 17.50, '2021-03-10');

-- Insert test transactions for first account
INSERT INTO transactions (account_id, transaction_date, posting_date, merchant_name, merchant_category, amount, description, reference_number, transaction_type, currency)
VALUES 
    (1, '2023-04-01 09:30:00', '2023-04-02 00:00:00', 'TESCO EXTRA KL', 'Groceries', -250.35, 'Weekly groceries', 'TX123456', 'PURCHASE', 'MYR'),
    (1, '2023-04-03 12:15:00', '2023-04-04 00:00:00', 'SHELL JALAN AMPANG', 'Fuel', -150.00, 'Fuel purchase', 'TX123457', 'PURCHASE', 'MYR'),
    (1, '2023-04-05 18:45:00', '2023-04-06 00:00:00', 'NETFLIX MALAYSIA', 'Entertainment', -54.90, 'Monthly subscription', 'TX123458', 'PURCHASE', 'MYR'),
    (1, '2023-04-10 20:30:00', '2023-04-11 00:00:00', 'LAZADA MALAYSIA', 'Shopping', -899.00, 'Electronics purchase', 'TX123459', 'PURCHASE', 'MYR'),
    (1, '2023-04-20 14:00:00', '2023-04-21 00:00:00', 'CIMB PAYMENT', 'Payment', 1000.00, 'Online payment', 'PY123456', 'PAYMENT', 'MYR');

-- Insert test transactions for second account
INSERT INTO transactions (account_id, transaction_date, posting_date, merchant_name, merchant_category, amount, description, reference_number, transaction_type, currency)
VALUES 
    (2, '2023-04-02 10:45:00', '2023-04-03 00:00:00', 'PARKSON PAVILION', 'Shopping', -1250.75, 'Clothing purchase', 'TX223456', 'PURCHASE', 'MYR'),
    (2, '2023-04-05 09:15:00', '2023-04-06 00:00:00', 'AGODA.COM', 'Travel', -2500.00, 'Hotel booking', 'TX223457', 'PURCHASE', 'MYR'),
    (2, '2023-04-08 19:30:00', '2023-04-09 00:00:00', 'GRAB MALAYSIA', 'Transportation', -25.50, 'Ride service', 'TX223458', 'PURCHASE', 'MYR'),
    (2, '2023-04-12 13:20:00', '2023-04-13 00:00:00', 'WATSON MIDVALLEY', 'Healthcare', -189.60, 'Health products', 'TX223459', 'PURCHASE', 'MYR'),
    (2, '2023-04-15 11:00:00', '2023-04-16 00:00:00', 'CIMB PAYMENT', 'Payment', 2000.00, 'Bank transfer payment', 'PY223456', 'PAYMENT', 'MYR');

-- Insert test transactions for third account
INSERT INTO transactions (account_id, transaction_date, posting_date, merchant_name, merchant_category, amount, description, reference_number, transaction_type, currency)
VALUES 
    (3, '2023-04-01 08:30:00', '2023-04-02 00:00:00', 'JAYA GROCER GURNEY', 'Groceries', -320.45, 'Monthly groceries', 'TX323456', 'PURCHASE', 'MYR'),
    (3, '2023-04-04 14:45:00', '2023-04-05 00:00:00', 'UNIQLO QUEENSBAY', 'Shopping', -459.80, 'Clothing purchase', 'TX323457', 'PURCHASE', 'MYR'),
    (3, '2023-04-09 12:00:00', '2023-04-10 00:00:00', 'SPOTIFY PREMIUM', 'Entertainment', -14.90, 'Monthly subscription', 'TX323458', 'PURCHASE', 'MYR'),
    (3, '2023-04-18 17:30:00', '2023-04-19 00:00:00', 'CIMB PAYMENT', 'Payment', 500.00, 'ATM payment', 'PY323456', 'PAYMENT', 'MYR');

-- Insert test billing cycles
INSERT INTO billing_cycles (account_id, start_date, end_date, statement_date, payment_due_date, previous_balance, total_purchases, total_payments, total_fees, total_interest, new_balance, minimum_payment)
VALUES 
    (1, '2023-03-16', '2023-04-15', '2023-04-15', '2023-04-25', 4500.00, 1354.25, 1000.00, 0.00, 145.75, 5000.00, 250.00),
    (2, '2023-03-21', '2023-04-20', '2023-04-20', '2023-04-30', 8500.00, 3965.85, 2000.00, 0.00, 284.15, 10750.00, 537.50),
    (3, '2023-03-26', '2023-04-25', '2023-04-25', '2023-05-10', 1500.00, 795.15, 500.00, 0.00, 41.35, 1836.50, 91.83);

-- Insert test payments
INSERT INTO payments (account_id, payment_date, amount, payment_method, reference_number)
VALUES 
    (1, '2023-04-20', 1000.00, 'ONLINE', 'REF123456'),
    (2, '2023-04-15', 2000.00, 'BANK_TRANSFER', 'REF223456'),
    (3, '2023-04-18', 500.00, 'CASH', 'REF323456');

-- Insert test interest calculations
INSERT INTO interest_calculations (account_id, cycle_id, calculation_date, principal_amount, interest_rate, interest_amount)
VALUES 
    (1, 1, '2023-04-15', 4500.00, 17.90, 145.75),
    (2, 2, '2023-04-20', 8500.00, 18.50, 284.15),
    (3, 3, '2023-04-25', 1500.00, 17.50, 41.35);

-- Insert test users
INSERT INTO users (username, password_hash, email, role)
VALUES 
    ('admin', '$2b$12$1tCY0TY6wDfg4FHnMq7rL.2mAk6KjANz3/GiXJp9m1eCARy9W3Iyi', 'admin@cimb.com', 'ADMIN'), -- password: admin123
    ('operator', '$2b$12$Yl8xmYLvbK7lCnM0RQO/UuQB4EF1UN4hM0vq3YP/XtlG.K/RNW5pG', 'operator@cimb.com', 'OPERATOR'); -- password: operator123

-- Insert test audit logs
INSERT INTO audit_logs (user_id, action, table_name, record_id, changes, ip_address)
VALUES 
    (1, 'INSERT', 'customers', 1, '{"first_name":"Ahmad","last_name":"Bin Abdullah"}', '192.168.1.100'),
    (1, 'UPDATE', 'accounts', 2, '{"credit_limit":"15000.00","previous":"10000.00"}', '192.168.1.100'),
    (2, 'INSERT', 'transactions', 5, '{"amount":"1000.00","transaction_type":"PAYMENT"}', '192.168.1.101');
    
show tables;
select * from customers;
select * from users;