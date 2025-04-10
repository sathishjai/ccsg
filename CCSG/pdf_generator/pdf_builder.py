import os
import logging
from datetime import datetime
import jinja2
import pdfkit
from pdf_generator.template_manager import TemplateManager
from utils.error_handler import PDFGenerationError

class PDFBuilder:
    """Builds PDF statements based on statement data and templates"""
    
    def __init__(self, bank_name, output_dir='output'):
        """
        Initialize PDF builder
        
        Args:
            bank_name: Name of the bank
            output_dir: Directory to save output PDF files
        """
        self.bank_name = bank_name.lower()
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_pdf(self, statement_data):
        """
        Generate PDF statement from statement data
        
        Args:
            statement_data: Processed statement data
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # Get language from statement data
            language = statement_data.get('language', 'EN')
            
            # Initialize template manager
            template_manager = TemplateManager(self.bank_name, language)
            template_path = template_manager.get_template_path()
            template_assets = template_manager.get_template_assets()
            
            # Prepare data for template
            template_data = {
                'statement': statement_data,
                'template': template_manager.get_template_data(),
                'translate': template_manager.translate,
                'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'assets': template_assets
            }
            
            # Load template with Jinja2
            template_loader = jinja2.FileSystemLoader(os.path.dirname(template_path))
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(os.path.basename(template_path))
            
            # Render HTML
            html_content = template.render(**template_data)
            
            # Create a temporary HTML file
            temp_html_path = os.path.join(self.output_dir, 'temp_statement.html')
            with open(temp_html_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)
            
            # Generate PDF filename
            customer_id = statement_data['customer']['customer_id']
            account_number = statement_data['account']['masked_account_number'].replace('-', '').replace('X', '')
            statement_date = statement_data['statement_period']['end_date'].strftime('%Y%m%d')
            pdf_filename = f"{self.bank_name}_statement_{customer_id}_{account_number}_{statement_date}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Convert HTML to PDF using pdfkit (wkhtmltopdf wrapper)
            options = {
                'page-size': 'A4',
                'margin-top': '10mm',
                'margin-right': '10mm',
                'margin-bottom': '10mm',
                'margin-left': '10mm',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            pdfkit.from_file(temp_html_path, pdf_path, options=options)
            
            # Clean up temporary HTML file
            os.remove(temp_html_path)
            
            logging.info(f"PDF statement generated: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logging.error(f"Error generating PDF: {str(e)}")
            raise PDFGenerationError(f"Failed to generate PDF statement: {str(e)}")
