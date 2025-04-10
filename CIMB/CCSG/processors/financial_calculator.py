class FinancialCalculator:
    @staticmethod
    def calculate_minimum_payment(balance, min_payment_rate=0.02):
        min_payment = balance * min_payment_rate
        return max(min_payment, 25.00)  # Minimum payment is greater of 2% or $25

    @staticmethod
    def calculate_interest(balance, apr):
        daily_rate = apr / 365
        return balance * daily_rate * 30  # Approximate monthly interest

    @staticmethod
    def get_statement_summary(transactions):
        total_purchases = sum(t.amount for t in transactions if t.amount > 0)
        total_payments = abs(sum(t.amount for t in transactions if t.amount < 0))
        
        return {
            'total_purchases': total_purchases,
            'total_payments': total_payments,
            'transaction_count': len(transactions)
        }