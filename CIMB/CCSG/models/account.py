from datetime import datetime

class Account:
    def __init__(self, account_id, customer_id, account_number, card_number, 
                 credit_limit, current_balance, statement_date, due_date):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.card_number = card_number
        self.credit_limit = credit_limit
        self.current_balance = current_balance
        self.statement_date = datetime.strptime(statement_date, '%Y-%m-%d').date()
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

    @property
    def available_credit(self):
        return self.credit_limit - self.current_balance

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'customer_id': self.customer_id,
            'account_number': self.account_number,
            'card_number': self.card_number,
            'credit_limit': self.credit_limit,
            'current_balance': self.current_balance,
            'statement_date': self.statement_date.strftime('%Y-%m-%d'),
            'due_date': self.due_date.strftime('%Y-%m-%d')
        }