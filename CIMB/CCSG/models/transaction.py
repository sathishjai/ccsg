from datetime import datetime

class Transaction:
    def __init__(self, transaction_id, account_id, transaction_date, post_date, 
                 description, amount, category):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d').date()
        self.post_date = datetime.strptime(post_date, '%Y-%m-%d').date()
        self.description = description
        self.amount = amount
        self.category = category

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'transaction_date': self.transaction_date.strftime('%Y-%m-%d'),
            'post_date': self.post_date.strftime('%Y-%m-%d'),
            'description': self.description,
            'amount': self.amount,
            'category': self.category
        }