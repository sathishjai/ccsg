class Transaction:
    """Transaction model representing credit card transaction data"""
    
    def __init__(self, transaction_data):
        """Initialize transaction with data from database"""
        self.transaction_id = transaction_data.get('transaction_id')
        self.account_number = transaction_data.get('account_number')
        self.transaction_date = transaction_data.get('transaction_date')
        self.posting_date = transaction_data.get('posting_date')
        self.description = transaction_data.get('description')
        self.amount = transaction_data.get('amount')
        self.transaction_type = transaction_data.get('transaction_type')
        self.mcc_code = transaction_data.get('mcc_code')
        self.reference_number = transaction_data.get('reference_number')
    
    def is_debit(self):
        """Check if transaction is a debit (charge)"""
        return self.amount > 0
    
    def is_credit(self):
        """Check if transaction is a credit (payment)"""
        return self.amount < 0
    
    def get_formatted_amount(self, currency="RM"):
        """Return formatted amount with currency symbol"""
        if self.is_debit():
            return f"{currency} {abs(self.amount):.2f}"
        else:
            return f"{currency} {abs(self.amount):.2f} CR"
    
    def get_category(self):
        """Get transaction category based on type and MCC code"""
        if self.transaction_type == 'Payment':
            return 'Payment'
        elif self.transaction_type == 'Fee':
            return 'Fee'
        elif self.transaction_type == 'Interest':
            return 'Interest'
        elif self.transaction_type == 'Purchase':
            # Categorize based on MCC code
            if self.mcc_code in ['5411', '5422', '5462']:
                return 'Groceries'
            elif self.mcc_code in ['5812', '5813', '5814']:
                return 'Dining'
            elif self.mcc_code in ['4121', '4111', '4112']:
                return 'Transportation'
            elif self.mcc_code in ['5311', '5651', '5691']:
                return 'Shopping'
            else:
                return 'Other Purchases'
        else:
            return 'Other'
    
    def to_dict(self):
        """Convert transaction data to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'transaction_date': self.transaction_date,
            'posting_date': self.posting_date,
            'description': self.description,
            'amount': self.amount,
            'formatted_amount': self.get_formatted_amount(),
            'transaction_type': self.transaction_type,
            'category': self.get_category(),
            'reference_number': self.reference_number
        }
