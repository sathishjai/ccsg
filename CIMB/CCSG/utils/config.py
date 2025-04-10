    def _load_config(self):
        default_config = {
            'database': {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'credit_card_db',
                'port': 3306
            },
            'pdf': {
                'output_dir': 'statements',
                'default_template': 'default'
            },
            'statement': {
                'min_payment_rate': 0.02,
                'default_apr': 0.1499
            }
        }