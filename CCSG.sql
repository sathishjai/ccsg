create database CCSG;
use CCSG;
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(255),
    Address VARCHAR(255),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20)
);
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT,
    CardNumber VARCHAR(16),
    AccountBalance DECIMAL(18, 2),
    MinimumPayment DECIMAL(18, 2),
    DueDate DATE,
    CONSTRAINT FK_Customer FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    TransactionDate DATE,
    Amount DECIMAL(18, 2),
    Description VARCHAR(255),
    TransactionType VARCHAR(50),
    CONSTRAINT FK_Account FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);
show tables;
select * from accounts;