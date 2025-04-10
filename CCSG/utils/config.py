import os
import json
import logging

class ConfigurationError(Exception):
    """Exception raised for configuration errors"""
    pass

def _load_config_file(config_file='config.json'):
    """Load configuration from JSON file"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_file)
    
    # Check if config file exists
    if not os.path.exists(config_path):
        # Create default config
        default_config = {
            'database': {
                'server': 'localhost',
                'database': 'credit_card_statements',
                'username': 'statement_user',
                'password': 'your_password',
                'connection_timeout': 30
            },
            'pdf': {
                'output_directory': 'output',
                'page_size': 'A4',
                'dpi': 300
            },
            'logging': {
                'level': 'INFO',
                'file': 'app.log'
            }
        }
        
        # Write default config
        with open(config_path, 'w') as config_file_obj:
            json.dump(default_config, config_file_obj, indent=4)
        
        logging.warning(f"Config file not found. Created default config at {config_path}")
        return default_config
    
    # Load existing config
    try:
        with open(config_path, 'r') as config_file_obj:
            return json.load(config_file_obj)
    except Exception as e:
        logging.error(f"Error loading config file: {str(e)}")
        raise ConfigurationError(f"Failed to load configuration: {str(e)}")

class Config:
    def __init__(self, config_file='config.json'):
        self._config = _load_config_file(config_file)
    
    def get_config(self):
        """Get full configuration"""
        return self._config

    def get_db_config(self):
        """Get database configuration"""
        return self._config.get('database', {})

    def get_pdf_config(self):
        """Get PDF generation configuration"""
        return self._config.get('pdf', {})

    def get_logging_config(self):
        """Get logging configuration"""
        return self._config.get('logging', {})
