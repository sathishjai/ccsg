-- Database Schema for Maybank Credit Card Statement Generator

-- Create Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    address_line1 NVARCHAR(100) NOT NULL,
    address_line2 NVARCHAR(100),
    city NVARCHAR(50) NOT NULL,
    state NVARCHAR(50) NOT NULL,
    postal_code NVARCHAR(10) NOT NULL,
    country NVARCHAR(50) NOT NULL DEFAULT 'Malaysia',
    email NVARCHAR(100),
    phone NVARCHAR(20),
    membership_since DATE NOT NULL,
    customer_type NVARCHAR(20) DEFAULT 'Regular'
);

-- Create Accounts Table
CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    account_number NVARCHAR(20) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    card_type NVARCHAR(50) NOT NULL,
    credit_limit DECIMAL(15, 2) NOT NULL,
    available_credit DECIMAL(15, 2) NOT NULL,
    current_balance DECIMAL(15, 2) NOT NULL,
    previous_balance DECIMAL(15, 2) NOT NULL,
    statement_date DATE NOT NULL,
    payment_due_date DATE NOT NULL,
    minimum_payment DECIMAL(15, 2) NOT NULL,
    annual_fee DECIMAL(15, 2) DEFAULT 0.00,
    interest_rate DECIMAL(5, 2) NOT NULL,
    language_preference NVARCHAR(10) DEFAULT 'EN', -- EN for English, MS for Malay
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create Transactions Table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    account_number NVARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    description NVARCHAR(200) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type NVARCHAR(20) NOT NULL, -- 'Purchase', 'Payment', 'Fee', 'Interest', etc.
    mcc_code NVARCHAR(10), -- Merchant Category Code
    reference_number NVARCHAR(50),
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);

-- Create Rewards Table
CREATE TABLE rewards (
    rewards_id INT PRIMARY KEY,
    account_number NVARCHAR(20) NOT NULL,
    points_earned INT NOT NULL DEFAULT 0,
    points_redeemed INT NOT NULL DEFAULT 0,
    points_balance INT NOT NULL DEFAULT 0,
    points_expiring INT DEFAULT 0,
    expiry_date DATE,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);

-- Create Statements Table
CREATE TABLE statements (
    statement_id INT PRIMARY KEY,
    account_number NVARCHAR(20) NOT NULL,
    statement_date DATE NOT NULL,
    statement_period_start DATE NOT NULL,
    statement_period_end DATE NOT NULL,
    opening_balance DECIMAL(15, 2) NOT NULL,
    closing_balance DECIMAL(15, 2) NOT NULL,
    total_payments DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_purchases DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_fees DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_interest DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    minimum_payment DECIMAL(15, 2) NOT NULL,
    payment_due_date DATE NOT NULL,
    pdf_generated BIT DEFAULT 0,
    generation_date DATETIME,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);

-- Create Indexes for better performance
CREATE INDEX idx_transactions_account_date ON transactions(account_number, posting_date);
CREATE INDEX idx_customers_name ON customers(last_name, first_name);
CREATE INDEX idx_statements_account_date ON statements(account_number, statement_date);
