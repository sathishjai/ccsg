# CIMB Credit Card Statement Generator

A Python application that generates credit card statements for CIMB Bank customers using a MySQL database backend.

## Features

- Customer management system
- Credit card tracking
- Transaction recording
- Statement generation in PDF format
- User-friendly GUI interface

## Requirements

- Python 3.7+
- MySQL Server 5.7+ or MariaDB 10.3+
- Required Python libraries:
  - mysql-connector-python
  - pandas
  - fpdf
  - tkinter
  - python-dotenv

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cimb-credit-card-statement-generator.git
   cd cimb-credit-card-statement-generator
   ```

2. Install required packages:
   ```
   pip install mysql-connector-python pandas fpdf python-dotenv
   ```

3. Create a `.env` file in the project root with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. The application will:
   - Connect to MySQL
   - Create the necessary database and tables if they don't exist
   - Populate the database with sample data
   - Launch the GUI interface

3. Using the GUI:
   - Select a customer from the dropdown
   - Select one of the customer's credit cards
   - Select a statement period
   - Click "Generate Statement" to create a PDF statement

4. The PDF will be saved in the current directory with the name format `CIMB_Statement_{id}.pdf`

## Database Structure

The application uses the following database tables:

- `customers`: Stores customer information
- `credit_cards`: Stores credit card information linked to customers
- `transactions`: Records all credit card transactions
- `statements`: Stores monthly statement information

## Sample Data

The application includes a function to generate sample data for testing purposes, including:
- 3 sample customers
- Multiple credit cards per customer
- Random transactions for each card
- Monthly statements for the year 2024

## Customization

You can modify the following aspects of the application:
- Database connection parameters in the `.env` file
- PDF generation format in the `StatementGenerator` class
- GUI appearance in the `CIMBCreditCardApp` class
# CIMB Credit Card Statement Generator - Test Cases

This document outlines test cases for the CIMB Credit Card Statement Generator application.

## Database Connection Tests

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| DB-01 | Connect to MySQL server with valid credentials | Connection established successfully | ✅ |
| DB-02 | Connect to MySQL server with invalid credentials | Application displays error message | ✅ |
| DB-03 | Create database if it doesn't exist | Database created successfully | ✅ |
| DB-04 | Create tables if they don't exist | Tables created successfully | ✅ |

## Sample Data Tests

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| DATA-01 | Generate sample customers | 3 customers added to database | ✅ |
| DATA-02 | Generate sample credit cards | Each customer has 1-2 credit cards | ✅ |
| DATA-03 | Generate sample transactions | 10-20 transactions per card | ✅ |
| DATA-04 | Generate sample statements | 12 monthly statements per card for 2024 | ✅ |

## GUI Tests

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| GUI-01 | Launch application | GUI displays correctly | ✅ |
| GUI-02 | Populate customer dropdown | Dropdown shows all customers | ✅ |
| GUI-03 | Select customer | Card dropdown populated with customer's cards | ✅ |
| GUI-04 | Select card | Statement dropdown populated with card's statements | ✅ |
| GUI-05 | Generate statement without selection | Warning message displayed | ✅ |

## Statement Generation Tests

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| GEN-01 | Generate PDF statement | PDF file created successfully | ✅ |
| GEN-02 | PDF contains customer information | Customer name, address, phone, email displayed | ✅ |
| GEN-03 | PDF contains card information | Card number, type, credit limit displayed | ✅ |
| GEN-04 | PDF contains statement summary | Statement date, due date, total amount, minimum payment displayed | ✅ |
| GEN-05 | PDF contains transaction details | All transactions for statement period displayed | ✅ |

## Edge Cases

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| EDGE-01 | No transactions for statement period | Statement generated with 0.00 total | ✅ |
| EDGE-02 | Very large number of transactions | All transactions displayed correctly | ✅ |
| EDGE-03 | Very large transaction amounts | Amounts formatted correctly | ✅ |
| EDGE-04 | Special characters in customer/merchant names | Characters displayed correctly in PDF | ✅ |

## Integration Tests

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| INT-01 | Complete workflow: select customer → card → statement → generate | PDF statement generated successfully | ✅ |
| INT-02 | Add new customer via database and refresh app | New customer appears in dropdown | ✅ |
| INT-03 | Add new transaction via database and generate statement | New transaction appears in statement | ✅ |

## Performance Tests

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| PERF-01 | Generate statement with 100+ transactions | Statement generated in under 5 seconds | ✅ |
| PERF-02 | Load application with 1000+ customers | Application loads in under 10 seconds | ✅ |

## Manual Test Procedure

1. Start the application by running `python main.py`
2. Verify the main window appears with customer dropdown
3. Select a customer from the dropdown
4. Verify credit card dropdown populates
5. Select a credit card
6. Verify statement dropdown populates
7. Select a statement period
8. Click "Generate Statement" button
9. Verify success message appears
10. Locate and open the generated PDF file
11. Verify all information in the PDF is correct

## Known Issues

| Issue ID | Description | Workaround |
|----------|-------------|------------|
| ISSUE-01 | PDF display may vary slightly between PDF viewers | Use Adobe Acrobat Reader for consistent results |
| ISSUE-02 | Application requires environment variables to be set | Create .env file before running |

## Test Data Reset

To reset the test data and start fresh:
1. Drop the `cimb_credit_card` database from MySQL
2. Restart the application

The application will recreate the database and sample data automatically.
## Troubleshooting

- If you encounter database connection issues, ensure your MySQL server is running and the credentials in the `.env` file are correct.
- If the GUI doesn't display properly, ensure you have Tkinter installed correctly.
- For PDF generation issues, ensure you have FPDF installed properly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.