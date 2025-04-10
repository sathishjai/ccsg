from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .template_manager import TemplateManager

class PDFBuilder:
    def __init__(self):
        self.template_manager = TemplateManager()
        self.styles = getSampleStyleSheet()

    def generate_statement(self, customer_data, transactions, statement_date, bank_name='default'):
        template = self.template_manager.get_template(bank_name)
        
        # Create PDF document
        filename = f"statement_{customer_data.customer_id}_{statement_date}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        # Build content
        content = []
        
        # Add header
        content.extend(template.build_header(customer_data))
        
        # Add account summary
        content.extend(template.build_account_summary(customer_data))
        
        # Add transactions
        content.extend(template.build_transactions_table(transactions))
        
        # Add footer
        content.extend(template.build_footer())
        
        # Generate PDF
        doc.build(content)
        return filename