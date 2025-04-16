from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import pymysql
from fpdf import FPDF
import os
import urllib.request
from decimal import Decimal
import datetime

app = Flask(__name__)
app.secret_key = "cimb_pdf_generator_secret_key"

# Setup folders
os.makedirs("pdfs", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("fonts", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Font mapping for different languages
FONT_MAPPING = {
    "en": "NotoSans-Regular.ttf",
    "ms": "NotoSansMalayalam-Regular.ttf", 
    "vi": "NotoSans-Regular.ttf",
    "tl": "NotoSans-Regular.ttf",
    "en-gb": "NotoSans-Regular.ttf",
    "th": "NotoSansThai-Regular.ttf"
}

# Download required fonts
def download_fonts():
    print("[↓] Downloading required fonts...")
    base_url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/"
    fonts = {
        "NotoSans-Regular.ttf": "NotoSans/NotoSans-Regular.ttf",
        "NotoSansMalayalam-Regular.ttf": "NotoSansMalayalam/NotoSansMalayalam-Regular.ttf",
        "NotoSansThai-Regular.ttf": "NotoSansThai/NotoSansThai-Regular.ttf"
    }
    
    for font_file, font_path in fonts.items():
        font_full_path = f"fonts/{font_file}"
        if not os.path.exists(font_full_path):
            try:
                url = f"{base_url}{font_path}"
                urllib.request.urlretrieve(url, font_full_path)
                print(f"[✓] Downloaded {font_file}")
            except Exception as e:
                print(f"[✖] Error downloading {font_file}: {e}")
                log_error(f"Error downloading font {font_file}: {str(e)}")

# Call font download on startup
download_fonts()

def log_error(message):
    with open("logs/cimb_pdf_error_log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def get_db_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="2001",
            database="cimb_db",
            cursorclass=pymysql.cursors.Cursor
        )
        return conn
    except Exception as e:
        log_error(f"Database connection error: {str(e)}")
        return None

def fetch_customer_info(cursor, customer_id=None, customer_name=None):
    try:
        if customer_id:
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        elif customer_name:
            cursor.execute("SELECT * FROM customers WHERE name LIKE %s", (f"%{customer_name}%",))
        else:
            return None
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching customer info: {str(e)}")
        return None

def fetch_statements(cursor, customer_id):
    try:
        cursor.execute("SELECT * FROM statements WHERE customer_id = %s", (customer_id,))
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching statements: {str(e)}")
        return None

def fetch_transactions(cursor, statement_id):
    try:
        cursor.execute("SELECT txn_date, description, amount, txn_type FROM transactions WHERE statement_id = %s", (statement_id,))
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching transactions: {str(e)}")
        return None

# Translation dictionary
translations = {
    "en": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "STATEMENT DATE",
        "STATEMENT PERIOD": "STATEMENT PERIOD",
        "Credit Card eStatement Campaign 2024": "Credit Card eStatement Campaign 2024",
        "Switch to eStatements...": "Switch to eStatements now and stand a chance to win exciting prizes! Go paperless to reduce your carbon footprint and enjoy hassle-free banking.",
        "ACCOUNT SUMMARY": "ACCOUNT SUMMARY",
        "TOTAL OUTSTANDING BALANCE": "TOTAL OUTSTANDING BALANCE",
        "MINIMUM PAYMENT DUE": "MINIMUM PAYMENT DUE",
        "PAYMENT DUE DATE": "PAYMENT DUE DATE",
        "REWARDS POINTS BALANCE": "REWARDS POINTS BALANCE",
        "PAYMENT & TRANSACTIONS SUMMARY": "PAYMENT & TRANSACTIONS SUMMARY",
        "TRANSACTION DETAILS": "TRANSACTION DETAILS",
        "Date": "Date",
        "Description": "Description",
        "Amount": "Amount",
        "Credit Limit": "Credit Limit",
        "Available Credit": "Available Credit"
    },
    "ms": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "TARIKH PENYATA",
        "STATEMENT PERIOD": "TEMPOH PENYATA",
        "Credit Card eStatement Campaign 2024": "Kempen ePenyata Kad Kredit 2024",
        "Switch to eStatements...": "Beralih kepada ePenyata dan berpeluang memenangi hadiah menarik! Kurangkan jejak karbon anda dan nikmati perbankan tanpa kerumitan.",
        "ACCOUNT SUMMARY": "RINGKASAN AKAUN",
        "TOTAL OUTSTANDING BALANCE": "JUMLAH BAKI TERHUTANG",
        "MINIMUM PAYMENT DUE": "BAYARAN MINIMUM",
        "PAYMENT DUE DATE": "TARIKH AKHIR BAYARAN",
        "REWARDS POINTS BALANCE": "BAKI MATA GANJARAN",
        "PAYMENT & TRANSACTIONS SUMMARY": "RINGKASAN PEMBAYARAN & TRANSAKSI",
        "TRANSACTION DETAILS": "BUTIRAN TRANSAKSI",
        "Date": "Tarikh",
        "Description": "Keterangan",
        "Amount": "Jumlah",
        "Credit Limit": "Had Kredit",
        "Available Credit": "Kredit Tersedia"
    },
    "vi": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "NGÀY SAO KÊ",
        "STATEMENT PERIOD": "KỲ SAO KÊ",
        "Credit Card eStatement Campaign 2024": "Chiến dịch Sao kê điện tử Thẻ tín dụng 2024",
        "Switch to eStatements...": "Chuyển sang sao kê điện tử để có cơ hội nhận giải thưởng! Giảm thiểu dấu chân carbon và trải nghiệm ngân hàng tiện lợi.",
        "ACCOUNT SUMMARY": "TÓM TẮT TÀI KHOẢN",
        "TOTAL OUTSTANDING BALANCE": "TỔNG SỐ DƯ NỢ",
        "MINIMUM PAYMENT DUE": "SỐ TIỀN THANH TOÁN TỐI THIỂU",
        "PAYMENT DUE DATE": "NGÀY HẾT HẠN THANH TOÁN",
        "REWARDS POINTS BALANCE": "SỐ DƯ ĐIỂM THƯỞNG",
        "PAYMENT & TRANSACTIONS SUMMARY": "TÓM TẮT GIAO DỊCH VÀ THANH TOÁN",
        "TRANSACTION DETAILS": "CHI TIẾT GIAO DỊCH",
        "Date": "Ngày",
        "Description": "Mô tả",
        "Amount": "Số tiền",
        "Credit Limit": "Hạn mức tín dụng",
        "Available Credit": "Tín dụng còn lại"
    },
    "tl": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "PETSA NG PAHAYAG",
        "STATEMENT PERIOD": "PANAHON NG PAHAYAG",
        "Credit Card eStatement Campaign 2024": "Kampanya ng eStatement ng Credit Card 2024",
        "Switch to eStatements...": "Lumipat sa eStatements at magkaroon ng pagkakataong manalo ng magagandang premyo! Mag-go green at gawing madali ang pagbabangko.",
        "ACCOUNT SUMMARY": "BUOD NG ACCOUNT",
        "TOTAL OUTSTANDING BALANCE": "KABUUANG BALANSENG NATITIRA",
        "MINIMUM PAYMENT DUE": "MINIMUM NA BAYAD",
        "PAYMENT DUE DATE": "PETSANG HULING BAYAD",
        "REWARDS POINTS BALANCE": "BALANSENG PUNTOS NG GANTIMPALA",
        "PAYMENT & TRANSACTIONS SUMMARY": "BUOD NG BAYAD AT TRANSAKSYON",
        "TRANSACTION DETAILS": "DETALYE NG TRANSAKSYON",
        "Date": "Petsa",
        "Description": "Paglalarawan",
        "Amount": "Halaga",
        "Credit Limit": "Limitasyon ng Credit",
        "Available Credit": "Magagamit na Credit"
    },
    "en-gb": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "STATEMENT DATE",
        "STATEMENT PERIOD": "STATEMENT PERIOD",
        "Credit Card eStatement Campaign 2024": "Credit Card eStatement Campaign 2024",
        "Switch to eStatements...": "Switch to eStatements now and stand a chance to win exciting prizes! Go paperless to reduce your carbon footprint and enjoy hassle-free banking.",
        "ACCOUNT SUMMARY": "ACCOUNT SUMMARY",
        "TOTAL OUTSTANDING BALANCE": "TOTAL OUTSTANDING BALANCE",
        "MINIMUM PAYMENT DUE": "MINIMUM PAYMENT DUE",
        "PAYMENT DUE DATE": "PAYMENT DUE DATE",
        "REWARDS POINTS BALANCE": "REWARDS POINTS BALANCE",
        "PAYMENT & TRANSACTIONS SUMMARY": "PAYMENT & TRANSACTIONS SUMMARY",
        "TRANSACTION DETAILS": "TRANSACTION DETAILS",
        "Date": "Date",
        "Description": "Description",
        "Amount": "Amount",
        "Credit Limit": "Credit Limit",
        "Available Credit": "Available Credit"
    },
    "th": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "วันที่ออกใบแจ้งยอด",
        "STATEMENT PERIOD": "ระยะเวลาใบแจ้งยอด",
        "Credit Card eStatement Campaign 2024": "แคมเปญ eStatement บัตรเครดิต 2024",
        "Switch to eStatements...": "เปลี่ยนมาใช้ eStatement ลุ้นรับของรางวัล! ลดคาร์บอนฟุตพริ้นท์และทำธุรกรรมง่ายขึ้น",
        "ACCOUNT SUMMARY": "สรุปบัญชี",
        "TOTAL OUTSTANDING BALANCE": "ยอดค้างชำระทั้งหมด",
        "MINIMUM PAYMENT DUE": "ยอดชำระขั้นต่ำ",
        "PAYMENT DUE DATE": "วันครบกำหนดชำระเงิน",
        "REWARDS POINTS BALANCE": "ยอดคะแนนสะสม",
        "PAYMENT & TRANSACTIONS SUMMARY": "สรุปการชำระเงินและรายการ",
        "TRANSACTION DETAILS": "รายละเอียดรายการ",
        "Date": "วันที่",
        "Description": "รายละเอียด",
        "Amount": "จำนวนเงิน",
        "Credit Limit": "วงเงินเครดิต",
        "Available Credit": "เครดิตคงเหลือ"
    },
}

def tr(key, lang):
    return translations.get(lang, translations["en"]).get(key, key)

def generate_pdf(customer, statement, transactions, lang="en"):
    try:
        # Get appropriate font for the language
        font_file = FONT_MAPPING.get(lang, "NotoSans-Regular.ttf")
        font_path = f"fonts/{font_file}"
        
        # Check if font exists
        if not os.path.exists(font_path):
            log_error(f"Font file not found: {font_path}")
            # Fall back to default font if specific font not available
            font_path = "fonts/NotoSans-Regular.ttf"
            if not os.path.exists(font_path):
                # Try to download default font as a last resort
                try:
                    url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"
                    urllib.request.urlretrieve(url, font_path)
                    print(f"[✓] Downloaded fallback font NotoSans-Regular.ttf")
                except Exception as e:
                    log_error(f"Error downloading fallback font: {str(e)}")
                    return None
        
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Noto", "", font_path, uni=True)
        pdf.set_font("Noto", "", 10)
        pdf.set_auto_page_break(auto=True, margin=15)

        name, address, card_no, acc_no, credit_limit, available_credit = customer[1:7]
        stmt_date, period_start, period_end, out_bal, min_due, due_date, points = statement[2:]

        # Header
        pdf.set_font("Noto", "", 14)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 10, tr("CIMB", lang), ln=True)

        pdf.set_font("Noto", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, f"{tr('STATEMENT DATE', lang)}: {stmt_date}", ln=True)
        pdf.cell(0, 6, f"{tr('STATEMENT PERIOD', lang)}: {period_start} - {period_end}", ln=True)

        # Customer Info
        pdf.ln(5)
        pdf.set_font("Noto", "", 12)
        pdf.cell(0, 8, name.upper(), ln=True)
        pdf.set_font("Noto", "", 10)
        for line in address.split('\n'):
            pdf.cell(0, 6, line, ln=True)
        pdf.cell(0, 6, f"Card No: {card_no}", ln=True)
        pdf.cell(0, 6, f"Account No: {acc_no}", ln=True)

        pdf.set_xy(140, 30)
        pdf.multi_cell(0, 6, f"CIMB VISA PLATINUM\n{tr('Credit Limit', lang)}: RM {float(credit_limit):,.2f}\n{tr('Available Credit', lang)}: RM {float(available_credit):,.2f}")

        # Campaign Banner
        pdf.set_y(70)
        pdf.set_fill_color(255, 230, 230)
        pdf.set_text_color(128, 0, 0)
        pdf.set_font("Noto", "", 11)
        pdf.multi_cell(0, 10, tr("Credit Card eStatement Campaign 2024", lang), fill=True)
        pdf.set_font("Noto", "", 10)
        pdf.multi_cell(0, 6, tr("Switch to eStatements...", lang), fill=True)

        # Account Summary
        pdf.ln(3)
        pdf.set_font("Noto", "", 12)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 8, tr("ACCOUNT SUMMARY", lang), ln=True)

        pdf.set_font("Noto", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(100, 6, f"{tr('TOTAL OUTSTANDING BALANCE', lang)}\nRM {float(out_bal):,.2f}", ln=False)
        pdf.cell(0, 6, f"{tr('MINIMUM PAYMENT DUE', lang)}\nRM {float(min_due):,.2f}", ln=True)

        pdf.cell(100, 6, f"{tr('PAYMENT DUE DATE', lang)}\n{due_date}", ln=False)
        pdf.cell(0, 6, f"{tr('REWARDS POINTS BALANCE', lang)}\n{int(points):,} pts", ln=True)

        # Transaction Summary
        pdf.ln(4)
        pdf.set_font("Noto", "", 12)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 8, tr("PAYMENT & TRANSACTIONS SUMMARY", lang), ln=True)

        categories = {
            "Previous Balance": 0.00,
            "Payments": 0.00,
            "Purchases": 0.00,
            "Cash Advances": 0.00,
            "Fees and Charges": 0.00,
            "Interest Charges": 0.00,
            "Current Balance": float(out_bal)
        }

        for txn in transactions:
            amount = float(txn[2])
            ttype = txn[3]
            if "Payment" in ttype:
                categories["Payments"] += amount
            elif "Purchase" in ttype:
                categories["Purchases"] += amount
            elif "Cash Advance" in ttype:
                categories["Cash Advances"] += amount
            elif "Fee" in ttype:
                categories["Fees and Charges"] += amount
            elif "Interest" in ttype:
                categories["Interest Charges"] += amount

        pdf.set_font("Noto", "", 10)
        for k, v in categories.items():
            sign = "+" if v > 0 and k != "Payments" else ""
            pdf.cell(120, 6, k)
            pdf.cell(0, 6, f"{sign} RM {abs(v):,.2f}", ln=True)

        # Transaction Details
        pdf.ln(4)
        pdf.set_font("Noto", "", 12)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 8, tr("TRANSACTION DETAILS", lang), ln=True)

        pdf.set_font("Noto", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(40, 6, tr("Date", lang))
        pdf.cell(100, 6, tr("Description", lang))
        pdf.cell(0, 6, tr("Amount", lang), ln=True)

        for txn in transactions:
            date, desc, amount, _ = txn
            pdf.cell(40, 6, str(date))
            pdf.cell(100, 6, str(desc))
            pdf.cell(0, 6, f"RM {float(amount):,.2f}", ln=True)

        filename = f"pdfs/{name.replace(' ', '_')}_Statement_{stmt_date}.pdf"
        pdf.output(filename)
        print(f"[✓] Generated: {filename}")
        return filename
    except Exception as e:
        log_error(f"Error generating PDF: {str(e)}")
        return None

@app.route('/')
def index():
    languages = {
        "en": "English",
        "ms": "Malay",
        "vi": "Vietnamese",
        "tl": "Tagalog",
        "en-gb": "English (UK)",
        "th": "Thai"
    }
    return render_template('index.html', languages=languages)

@app.route('/search', methods=['POST'])
def search():
    lang_code = request.form.get('language', 'en')
    search_type = request.form.get('search_type')
    search_value = request.form.get('search_value')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    if search_type == "id":
        customers = fetch_customer_info(cursor, customer_id=search_value)
    else:
        customers = fetch_customer_info(cursor, customer_name=search_value)
    
    conn.close()
    
    if not customers:
        flash("No customers found.", "error")
        return redirect(url_for('index'))
    
    return render_template('customer_list.html', customers=customers, lang_code=lang_code)

@app.route('/statements/<customer_id>/<lang_code>')
def show_statements(customer_id, lang_code):
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    customer = fetch_customer_info(cursor, customer_id=customer_id)
    if not customer or len(customer) == 0:
        conn.close()
        flash("Customer not found.", "error")
        return redirect(url_for('index'))
    
    statements = fetch_statements(cursor, customer_id)
    conn.close()
    
    if not statements:
        flash("No statements found for this customer.", "error")
        return redirect(url_for('index'))
    
    return render_template('statements.html', customer=customer[0], statements=statements, lang_code=lang_code)

@app.route('/generate/<customer_id>/<statement_id>/<lang_code>')
def generate_statement(customer_id, statement_id, lang_code):
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    customer = fetch_customer_info(cursor, customer_id=customer_id)
    if not customer or len(customer) == 0:
        conn.close()
        flash("Customer not found.", "error")
        return redirect(url_for('index'))
    
    statement = None
    statements = fetch_statements(cursor, customer_id)
    if statements:
        for stmt in statements:
            if str(stmt[0]) == statement_id:
                statement = stmt
                break
    
    if not statement:
        conn.close()
        flash("Statement not found.", "error")
        return redirect(url_for('index'))
    
    transactions = fetch_transactions(cursor, statement_id)
    conn.close()
    
    if not transactions:
        flash("No transactions found for this statement.", "warning")
    
    filename = generate_pdf(customer[0], statement, transactions, lang=lang_code)
    
    if not filename:
        flash("Error generating PDF. Check logs for details.", "error")
        return redirect(url_for('index'))
    
    flash(f"PDF generated successfully: {filename}", "success")
    return redirect(url_for('download_pdf', filename=os.path.basename(filename)))

@app.route('/download/<filename>')
def download_pdf(filename):
    return send_from_directory('pdfs', filename, as_attachment=True)

@app.route('/view_customers')
def view_customers():
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching all customers: {str(e)}")
        customers = []
    
    conn.close()
    
    return render_template('all_customers.html', customers=customers)

if __name__ == "__main__":
    app.run(debug=True)