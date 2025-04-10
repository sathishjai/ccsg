from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

class Template:
    def build_header(self, customer_data):
        elements = []
        # Add bank logo and header information
        header_text = f"""
        <para align=center>
        <font size=20>Credit Card Statement</font><br/>
        <font size=12>{customer_data.full_name}<br/>
        {customer_data.address}<br/>
        {customer_data.city}, {customer_data.state} {customer_data.zip_code}
        </font>
        </para>
        """
        elements.append(Paragraph(header_text, ParagraphStyle('Header')))
        elements.append(Spacer(1, 20))
        return elements

    def build_account_summary(self, account_data):
        elements = []
        # Create account summary table
        data = [
            ['Account Number:', account_data.account_number],
            ['Statement Date:', account_data.statement_date],
            ['Due Date:', account_data.due_date],
            ['Credit Limit:', f"${account_data.credit_limit:,.2f}"],
            ['Current Balance:', f"${account_data.current_balance:,.2f}"]
        ]
        
        table = Table(data, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        return elements

    def build_transactions_table(self, transactions):
        elements = []
        # Create transactions table
        header = ['Date', 'Description', 'Amount']
        data = [header]
        
        for trans in transactions:
            data.append([
                trans.transaction_date,
                trans.description,
                f"${trans.amount:,.2f}"
            ])
            
        table = Table(data, colWidths=[100, 300, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def build_footer(self):
        elements = []
        footer_text = """
        <para align=center>
        <font size=8>For questions about your statement, please contact customer service.<br/>
        1-800-555-0000 | www.bank.com</font>
        </para>
        """
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer')))
        return elements