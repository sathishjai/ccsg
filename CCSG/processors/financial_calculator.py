class FinancialCalculator:
    """Calculates financial data for credit card statement"""
    
    @staticmethod
    def calculate_minimum_payment(current_balance, minimum_payment_percentage=5.0, minimum_amount=10.0):
        """
        Calculate minimum payment based on current balance
        
        Args:
            current_balance: The current outstanding balance
            minimum_payment_percentage: The percentage for minimum payment (default 5%)
            minimum_amount: The minimum amount regardless of percentage (default RM10)
            
        Returns:
            The calculated minimum payment amount
        """
        calculated_amount = current_balance * (minimum_payment_percentage / 100)
        return max(calculated_amount, minimum_amount) if current_balance > 0 else 0
    
    @staticmethod
    def calculate_interest(previous_balance, payments, interest_rate, days_in_month=30):
        """
        Calculate interest charges based on average daily balance
        
        Args:
            previous_balance: Previous statement balance
            payments: List of payment transactions with amounts and dates
            interest_rate: Annual interest rate percentage
            days_in_month: Number of days in the billing cycle
            
        Returns:
            The calculated interest amount
        """
        # Simple implementation using average daily balance method
        # In a real application, this would be more complex with exact day calculations
        
        # Calculate average daily balance
        total_balance = previous_balance * days_in_month
        
        # Subtract payments based on when they were made in the cycle
        for payment in payments:
            # Get day of payment in the cycle (assume payment.posting_date is a datetime object)
            if hasattr(payment, 'posting_date') and payment.posting_date:
                days_remaining = days_in_month - payment.posting_date.day
                total_balance -= abs(payment.amount) * days_remaining
        
        average_daily_balance = total_balance / days_in_month
        
        # Calculate monthly interest
        monthly_rate = interest_rate / 12 / 100
        interest = average_daily_balance * monthly_rate
        
        return round(interest, 2)
    
    @staticmethod
    def calculate_statement_summary(transactions):
        """
        Calculate statement summary from transactions
        
        Args:
            transactions: List of transaction objects
            
        Returns:
            Dictionary with summary information
        """
        summary = {
            'total_debits': 0,
            'total_credits': 0,
            'total_fees': 0,
            'total_interest': 0,
            'total_purchases': 0,
            'transactions_count': len(transactions)
        }
        
        for transaction in transactions:
            amount = abs(transaction.amount)
            
            if transaction.transaction_type == 'Fee':
                summary['total_fees'] += amount
                summary['total_debits'] += amount
            elif transaction.transaction_type == 'Interest':
                summary['total_interest'] += amount
                summary['total_debits'] += amount
            elif transaction.transaction_type == 'Purchase':
                summary['total_purchases'] += amount
                summary['total_debits'] += amount
            elif transaction.transaction_type == 'Payment':
                summary['total_credits'] += amount
        
        return summary
