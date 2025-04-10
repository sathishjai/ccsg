import logging
import sys
from datetime import datetime

class ErrorHandler:
    @staticmethod
    def setup_logging():
        logging.basicConfig(
            filename=f'logs/error_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def handle_error(error, exit_program=True):
        error_message = str(error)
        logging.error(error_message)
        print(f"Error: {error_message}", file=sys.stderr)
        
        if exit_program:
            sys.exit(1)