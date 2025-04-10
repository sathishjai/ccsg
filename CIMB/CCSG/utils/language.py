class Language:
    _translations = {
        'en': {
            'statement_header': 'Credit Card Statement',
            'account_number': 'Account Number',
            'statement_date': 'Statement Date',
            'due_date': 'Due Date',
            'credit_limit': 'Credit Limit',
            'current_balance': 'Current Balance',
            'minimum_payment': 'Minimum Payment Due',
            'transaction_date': 'Transaction Date',
            'description': 'Description',
            'amount': 'Amount',
            'customer_service': 'For customer service, please call'
        },
        'es': {
            'statement_header': 'Estado de Cuenta de Tarjeta de Crédito',
            'account_number': 'Número de Cuenta',
            'statement_date': 'Fecha del Estado',
            'due_date': 'Fecha de Vencimiento',
            'credit_limit': 'Límite de Crédito',
            'current_balance': 'Saldo Actual',
            'minimum_payment': 'Pago Mínimo',
            'transaction_date': 'Fecha de Transacción',
            'description': 'Descripción',
            'amount': 'Monto',
            'customer_service': 'Para servicio al cliente, llame al'
        }
    }

    @staticmethod
    def get_text(key, language='en'):
        if language not in Language._translations:
            language = 'en'
        return Language._translations[language].get(key, key)