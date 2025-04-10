from datetime import datetime

class Account:
    """Account model representing credit card account data"""
    
    def __init__(self, account_data):
        """Initialize account with data from database"""
        self.account_id = account_data.get('account_id')
        self.account_number = account_data.get('account_number')
        self.customer_id = account_data.get('customer_id')
        self.card_type = account_data.get('card_type')
        self.credit_limit = account_data.get('credit_limit')
        self.available_credit = account_data.get('available_credit')
        self.current_balance = account_data.get('current_balance')
        self.previous_balance = account_data.get('previous_balance')
        self.statement_date = account_data.get('statement_date')
        self.payment_due_date = account_data.get('payment_due_date')
        self.minimum_payment = account_data.get('minimum_payment')
        self.annual_fee = account_data.get('annual_fee')
        self.interest_rate = account_data.get('interest_rate')
        self.language_preference = account_data.get('language_preference')
        
    def get_masked_account_number(self):
        """Return the masked account number for display"""
        if not self.account_number:
            return ""
        
        parts = self.account_number.split('-')
        if len(parts) == 4:
            # Mask middle parts
            masked_parts = [parts[0], 'XXXX', 'XXXX', parts[3]]
            return '-'.join(masked_parts)
        else:
            # If format is not as expected, mask everything except last 4 digits
            raw_number = self.account_number.replace('-', '')
            return 'XXXX-XXXX-XXXX-' + raw_number[-4:]
    
    def get_statement_period(self, end_date=None):
        """Calculate statement period based on statement date"""
        if end_date is None:
            end_date = self.statement_date
            
        # If end_date is a string, convert to datetime
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        # Calculate start date (usually one month before end date)
        if end_date.month == 1:
            start_month = 12
            start_year = end_date.year - 1
        else:
            start_month = end_date.month - 1
            start_year = end_date.year
            
        # Adjust for different month lengths
        start_day = min(end_date.day, 28)  # Safe for February
        
        # Create start date
        start_date = datetime(start_year, start_month, start_day).date()
        
        return {
            'start_date': start_date,
            'end_date': end_date
        }
    
    def to_dict(self):
        """Convert account data to dictionary"""
        return {
            'account_number': self.account_number,
            'masked_account_number': self.get_masked_account_number(),
            'card_type': self.card_type,
            'credit_limit': self.credit_limit,
            'available_credit': self.available_credit,
            'current_balance': self.current_balance,
            'previous_balance': self.previous_balance,
            'statement_date': self.statement_date,
            'payment_due_date': self.payment_due_date,
            'minimum_payment': self.minimum_payment,
            'annual_fee': self.annual_fee,
            'interest_rate': self.interest_rate,
            'language_preference': self.language_preference
        }
