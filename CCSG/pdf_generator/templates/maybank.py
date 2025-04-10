def get_template_data(language='EN'):
    """
    Get template data for Maybank credit card statements
    
    Args:
        language: Language code ('EN' for English, 'MS' for Malay)
        
    Returns:
        Dictionary with template configuration
    """
    template = {
        'bank_name': 'Maybank',
        'logo_path': 'maybank_logo.png',
        'primary_color': '#FFC800',  # Maybank yellow
        'secondary_color': '#000000',  # Black
        'font_family': 'Arial, Helvetica, sans-serif',
        'header_font_family': 'Arial, Helvetica, sans-serif',
        'footer_text': 'Maybank Berhad (Registration No. 196001000142)',
        'contact_info': {
            'EN': {
                'address': 'Maybank Card Centre\nMenara Maybank, 100 Jalan Tun Perak\n50050 Kuala Lumpur',
                'phone': 'Customer Service Hotline: 1300-88-6688',
                'email': 'service@maybank.com.my',
                'website': 'www.maybank.com.my'
            },
            'MS': {
                'address': 'Pusat Kad Maybank\nMenara Maybank, 100 Jalan Tun Perak\n50050 Kuala Lumpur',
                'phone': 'Talian Khidmat Pelanggan: 1300-88-6688',
                'email': 'service@maybank.com.my',
                'website': 'www.maybank.com.my'
            }
        },
        'sections': [
            {
                'name': 'header',
                'order': 1,
                'title': {
                    'EN': 'CREDIT CARD STATEMENT',
                    'MS': 'PENYATA KAD KREDIT'
                }
            },
            {
                'name': 'summary',
                'order': 2,
                'title': {
                    'EN': 'STATEMENT SUMMARY',
                    'MS': 'RINGKASAN PENYATA'
                }
            },
            {
                'name': 'account_details',
                'order': 3,
                'title': {
                    'EN': 'ACCOUNT DETAILS',
                    'MS': 'BUTIRAN AKAUN'
                }
            },
            {
                'name': 'transactions',
                'order': 4,
                'title': {
                    'EN': 'TRANSACTION DETAILS',
                    'MS': 'BUTIRAN TRANSAKSI'
                }
            },
            {
                'name': 'rewards',
                'order': 5,
                'title': {
                    'EN': 'REWARDS SUMMARY',
                    'MS': 'RINGKASAN GANJARAN'
                }
            },
            {
                'name': 'payment_instructions',
                'order': 6,
                'title': {
                    'EN': 'PAYMENT INFORMATION',
                    'MS': 'MAKLUMAT PEMBAYARAN'
                }
            },
            {
                'name': 'footer',
                'order': 7,
                'title': {
                    'EN': 'IMPORTANT INFORMATION',
                    'MS': 'MAKLUMAT PENTING'
                }
            }
        ],
        'transaction_headers': {
            'EN': {
                'date': 'Date',
                'description': 'Description',
                'amount': 'Amount (RM)'
            },
            'MS': {
                'date': 'Tarikh',
                'description': 'Keterangan',
                'amount': 'Amaun (RM)'
            }
        },
        'payment_instructions': {
            'EN': [
                'Pay online through Maybank2u',
                'Cash/cheque payment at any Maybank branch',
                'Payment via ATM',
                'JomPAY Online (Biller Code: 50643)'
            ],
            'MS': [
                'Bayar dalam talian melalui Maybank2u',
                'Bayaran tunai/cek di mana-mana cawangan Maybank',
                'Pembayaran melalui ATM',
                'JomPAY Dalam Talian (Kod Pengebil: 50643)'
            ]
        }
    }
    
    return template
