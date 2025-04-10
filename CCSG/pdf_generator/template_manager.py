import os
import logging
from utils.error_handler import TemplateError
from utils.language import get_translation

class TemplateManager:
    """Manages templates for different banks and languages"""
    
    def __init__(self, bank_name, language='EN'):
        """
        Initialize template manager for specific bank and language
        
        Args:
            bank_name: Name of the bank (e.g., 'maybank')
            language: Language code (default 'EN' for English)
        """
        self.bank_name = bank_name.lower()
        self.language = language.upper()
        self.translations = get_translation(self.language)
        
        # Load bank-specific template module
        try:
            template_module = __import__(f'pdf_generator.templates.{self.bank_name}',
                                        fromlist=['get_template_data'])
            self.template_data = template_module.get_template_data(self.language)
        except ImportError:
            logging.error(f"Template for bank '{bank_name}' not found")
            raise TemplateError(f"Template for bank '{bank_name}' not found")
        except Exception as e:
            logging.error(f"Error loading template: {str(e)}")
            raise TemplateError(f"Error loading template: {str(e)}")
    
    def get_template_path(self):
        """Get path to HTML template file"""
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', self.bank_name)
        template_file = f"statement_template_{self.language.lower()}.html"
        template_path = os.path.join(template_dir, template_file)
        
        if not os.path.exists(template_path):
            logging.error(f"Template file not found: {template_path}")
            raise TemplateError(f"Template file not found: {template_path}")
        
        return template_path
    
    def get_template_assets(self):
        """Get dictionary of template assets (images, logos, etc.)"""
        asset_dir = os.path.join(os.path.dirname(__file__), 'templates', self.bank_name, 'assets')
        assets = {}
        
        # Load all assets from directory
        if os.path.exists(asset_dir):
            for filename in os.listdir(asset_dir):
                file_path = os.path.join(asset_dir, filename)
                if os.path.isfile(file_path):
                    assets[filename] = file_path
        
        return assets
    
    def get_template_data(self):
        """Get template data including text and formatting options"""
        return self.template_data
    
    def translate(self, key):
        """Translate a key to the current language"""
        return self.translations.get(key, key)
