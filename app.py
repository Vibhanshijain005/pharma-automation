"""
Pharmacy Automation System - Complete Flask Backend
A fully functional pharmacy management system.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from werkzeug.utils import secure_filename

# ==================== APP & DATABASE CONFIG ====================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pharmacy-secret-key-change-in-production'

# Setup database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'pharmacy.db').replace('\\', '/')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Directories for uploads and invoices
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMG_DIR = os.path.join(STATIC_DIR, 'images')
INVOICE_DIR = os.path.join(BASE_DIR, 'instance', 'invoices')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(INVOICE_DIR, exist_ok=True)

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================
class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Supplier(db.Model):
    """Supplier model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    medicines = db.relationship('Medicine', backref='supplier', lazy=True)


class Customer(db.Model):
    """Customer model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))


class Medicine(db.Model):
    """Medicine/Product model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    expiry_date = db.Column(db.Date)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))


class Sale(db.Model):
    """Sale/Transaction model"""
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200))
    total = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Purchase(db.Model):
    """Purchase order model"""
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    total = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== AUTHENTICATION & DECORATORS ====================
def login_required(role=None):
    """Decorator to check login and optional role authorization"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') not in role:
                flash('Access denied. Insufficient permissions.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return wrapped
    return decorator


# ==================== DATABASE INITIALIZATION ====================
def init_database():
    """Initialize database with tables and default admin"""
    with app.app_context():
        try:
            db.create_all()
            # Create default admin if doesn't exist
            if not User.query.filter_by(email='admin@pharma.local').first():
                admin = User(
                    name='Admin',
                    email='admin@pharma.local',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin created: admin@pharma.local / admin123")
            print("✓ Database initialized successfully")
        except Exception as e:
            print(f"⚠ Database error: {e}")


# ==================== ROUTES ====================
@app.route('/')
def index():
    """Home - redirect to dashboard or login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password required', 'warning')
            return render_template('login.html')
        
        try:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['role'] = user.role
                session['user_name'] = user.name
                flash(f'Welcome {user.name}!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid email or password', 'danger')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'customer')
        
        # Validation
        if not all([name, email, password]):
            flash('All fields required', 'warning')
            return render_template('register.html')
        
        try:
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'warning')
                return render_template('register.html')
            
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration error: {str(e)}', 'danger')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required()
def dashboard():
    """Dashboard with statistics"""
    try:
        total_medicines = Medicine.query.count()
        low_stock = Medicine.query.filter(Medicine.quantity <= Medicine.reorder_level).count()
        
        today = datetime.utcnow().date()
        upcoming_expiry = Medicine.query.filter(
            Medicine.expiry_date <= today + timedelta(days=30)
        ).count()
        
        sales_today = Sale.query.filter(
            Sale.date >= datetime.combine(today, datetime.min.time())
        ).count()
        
        recent_sales = Sale.query.order_by(Sale.date.desc()).limit(5).all()
        
        return render_template('dashboard.html',
                             total_medicines=total_medicines,
                             low_stock=low_stock,
                             upcoming_expiry=upcoming_expiry,
                             sales_today=sales_today,
                             recent_sales=recent_sales)
    except Exception as e:
        flash(f'Dashboard error: {str(e)}', 'danger')
        return render_template('dashboard.html',
                             total_medicines=total_medicines,
                             low_stock=low_stock,
                             upcoming_expiry=upcoming_expiry,
                             sales_today=sales_today,
                             recent_sales=recent_sales)


@app.route('/medicines')
@login_required()
def medicines():
    """List medicines with search"""
    try:
        search = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        
        query = Medicine.query
        if search:
            query = query.filter(Medicine.name.ilike(f'%{search}%'))
        
        medicines_page = query.order_by(Medicine.name).paginate(page=page, per_page=10)
        
        return render_template('medicines.html',
                             medicines=medicines_page,
                             search=search)
    except Exception as e:
        flash(f'Error loading medicines: {str(e)}', 'danger')
        return render_template('medicines.html', medicines=None, search='')


@app.route('/medicine/add', methods=['GET', 'POST'])
@login_required(role=['admin', 'pharmacist'])
def add_medicine():
    """Add new medicine"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            category = request.form.get('category', '').strip()
            price = float(request.form.get('price', 0) or 0)
            quantity = int(request.form.get('quantity', 0) or 0)
            expiry = request.form.get('expiry_date')
            
            if not name:
                flash('Medicine name required', 'warning')
                return render_template('medicine_form.html')
            
            expiry_date = None
            if expiry:
                try:
                    expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
                except:
                    flash('Invalid date format', 'warning')
                    return render_template('medicine_form.html')
            
            medicine = Medicine(
                name=name,
                category=category,
                price=price,
                quantity=quantity,
                expiry_date=expiry_date
            )
            # attach supplier if provided
            supplier_id = request.form.get('supplier_id')
            if supplier_id:
                try:
                    medicine.supplier_id = int(supplier_id)
                except:
                    pass
            db.session.add(medicine)
            db.session.commit()
            flash('Medicine added successfully', 'success')
            return redirect(url_for('medicines'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('medicine_form.html', suppliers=suppliers)


@app.route('/medicine/edit/<int:id>', methods=['GET', 'POST'])
@login_required(role=['admin', 'pharmacist'])
def edit_medicine(id):
    """Edit medicine"""
    try:
        medicine = Medicine.query.get_or_404(id)
        
        if request.method == 'POST':
            medicine.name = request.form.get('name', '').strip()
            medicine.category = request.form.get('category', '').strip()
            medicine.price = float(request.form.get('price', 0) or 0)
            medicine.quantity = int(request.form.get('quantity', 0) or 0)
            
            expiry = request.form.get('expiry_date')
            if expiry:
                try:
                    medicine.expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
                except:
                    flash('Invalid date', 'warning')
                    return render_template('medicine_form.html', med=medicine)
            # update supplier
            supplier_id = request.form.get('supplier_id')
            if supplier_id:
                try:
                    medicine.supplier_id = int(supplier_id)
                except:
                    medicine.supplier_id = None
            
            db.session.commit()
            flash('Medicine updated', 'success')
            return redirect(url_for('medicines'))
        
        suppliers = Supplier.query.order_by(Supplier.name).all()
        return render_template('medicine_form.html', med=medicine, suppliers=suppliers)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('medicines'))


@app.route('/medicine/delete/<int:id>', methods=['POST'])
@login_required(role=['admin'])
def delete_medicine(id):
    """Delete medicine"""
    try:
        medicine = Medicine.query.get_or_404(id)
        db.session.delete(medicine)
        db.session.commit()
        flash('Medicine deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Delete error: {str(e)}', 'danger')
    
    return redirect(url_for('medicines'))


@app.route('/billing', methods=['GET', 'POST'])
@login_required(role=['admin', 'pharmacist'])
def billing():
    """Billing and invoice"""
    try:
        medicines = Medicine.query.order_by(Medicine.name).all()
        if request.method == 'POST':
            action = request.form.get('action', 'save')
            customer_name = request.form.get('customer_name', '').strip()

            if not customer_name:
                flash('Customer name required', 'warning')
                return render_template('billing.html', medicines=medicines)

            items = []
            total = 0.0

            # Collect items and reduce stock
            for med in medicines:
                qty_str = request.form.get(f'qty_{med.id}', '0')
                try:
                    qty = int(qty_str or 0)
                except:
                    continue

                if qty > 0:
                    if qty > med.quantity:
                        flash(f'Insufficient stock for {med.name}', 'warning')
                        return render_template('billing.html', medicines=medicines)

                    line_total = qty * med.price
                    total += line_total
                    items.append((med, qty, line_total))
                    med.quantity -= qty

            if not items:
                flash('Select at least one item', 'warning')
                return render_template('billing.html', medicines=medicines)

            # Ensure customer exists
            customer = Customer.query.filter_by(name=customer_name).first()
            if not customer:
                customer = Customer(name=customer_name)
                db.session.add(customer)

            # Create sale
            sale = Sale(customer_name=customer_name, total=total)
            db.session.add(sale)
            db.session.commit()

            # Redirect to sale detail page which shows total and allows PDF download
            flash('Invoice created successfully', 'success')
            return redirect(url_for('sale_detail', id=sale.id))

        return render_template('billing.html', medicines=medicines)
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return render_template('billing.html', medicines=medicines)



@app.route('/sale/<int:id>')
@login_required()
def sale_detail(id):
    s = Sale.query.get_or_404(id)
    return render_template('sale_detail.html', sale=s)


@app.route('/sale/<int:id>/invoice')
@login_required()
def sale_invoice(id):
    s = Sale.query.get_or_404(id)

    # generate simple PDF (customer, date, total)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    story.append(Paragraph("<b>PHARMACY INVOICE</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Invoice ID:</b> {s.id}", styles['Normal']))
    story.append(Paragraph(f"<b>Customer:</b> {s.customer_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {s.date.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>TOTAL:</b> PKR {s.total:.2f}", styles['Heading2']))
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'invoice_{s.id}.pdf', mimetype='application/pdf')


@app.route('/customers')
@login_required()
def customers():
    """View customers"""
    try:
        cust_list = Customer.query.order_by(Customer.name).all()
        return render_template('customers.html', customers=cust_list)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('customers.html', customers=[])


@app.route('/customer/add', methods=['POST'])
@login_required(role=['admin', 'pharmacist'])
def add_customer():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    if not name:
        flash('Customer name required', 'warning')
        return redirect(url_for('customers'))
    try:
        c = Customer(name=name, email=email, phone=phone, address=address)
        db.session.add(c)
        db.session.commit()
        flash('Customer added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding customer: {e}', 'danger')
    return redirect(url_for('customers'))


@app.route('/customer/delete/<int:id>', methods=['POST'])
@login_required(role=['admin'])
def delete_customer(id):
    try:
        c = Customer.query.get_or_404(id)
        db.session.delete(c)
        db.session.commit()
        flash('Customer deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting customer: {e}', 'danger')
    return redirect(url_for('customers'))


@app.route('/suppliers')
@login_required()
def suppliers():
    """View suppliers"""
    try:
        supp_list = Supplier.query.order_by(Supplier.name).all()
        return render_template('suppliers.html', suppliers=supp_list)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('suppliers.html', suppliers=[])


@app.route('/supplier/add', methods=['POST'])
@login_required(role=['admin', 'pharmacist'])
def add_supplier():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    if not name:
        flash('Supplier name required', 'warning')
        return redirect(url_for('suppliers'))

    try:
        s = Supplier(name=name, email=email, phone=phone, address=address)
        db.session.add(s)
        db.session.commit()
        flash('Supplier added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding supplier: {e}', 'danger')

    return redirect(url_for('suppliers'))


@app.route('/supplier/edit/<int:id>', methods=['GET', 'POST'])
@login_required(role=['admin', 'pharmacist'])
def edit_supplier(id):
    s = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        s.name = request.form.get('name', s.name).strip()
        s.email = request.form.get('email', s.email).strip()
        s.phone = request.form.get('phone', s.phone).strip()
        s.address = request.form.get('address', s.address).strip()
        try:
            db.session.commit()
            flash('Supplier updated', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating supplier: {e}', 'danger')
        return redirect(url_for('suppliers'))

    return render_template('supplier_form.html', supplier=s)


@app.route('/supplier/delete/<int:id>', methods=['POST'])
@login_required(role=['admin'])
def delete_supplier(id):
    try:
        s = Supplier.query.get_or_404(id)
        db.session.delete(s)
        db.session.commit()
        flash('Supplier deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting supplier: {e}', 'danger')
    return redirect(url_for('suppliers'))


@app.route('/reports')
@login_required(role=['admin', 'pharmacist'])
def reports():
    """Sales reports"""
    try:
        period = request.args.get('period', 'daily')
        today = datetime.utcnow().date()
        
        if period == 'monthly':
            start = datetime(today.year, today.month, 1)
        else:
            start = datetime.combine(today, datetime.min.time())
        
        sales = Sale.query.filter(Sale.date >= start).order_by(Sale.date.desc()).all()
        total = sum(s.total for s in sales) if sales else 0
        
        return render_template('reports.html', sales=sales, total=total, period=period)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('reports.html', sales=[], total=0, period='daily')


@app.route('/settings', methods=['GET', 'POST'])
@login_required(role=['admin'])
def settings():
    """Application settings - upload logo and basic prefs"""
    if request.method == 'POST':
        pharmacy_name = request.form.get('pharmacy_name')
        contact_email = request.form.get('contact_email')

        # handle logo upload
        logo = request.files.get('logo')
        if logo and logo.filename:
            filename = secure_filename(logo.filename)
            dest = os.path.join(IMG_DIR, 'logo' + os.path.splitext(filename)[1])
            logo.save(dest)
            flash('Logo uploaded', 'success')
        else:
            flash('Settings saved', 'success')

        return redirect(url_for('settings'))

    # show settings page
    logo_path = None
    # try to locate a logo file
    for f in os.listdir(IMG_DIR):
        if f.startswith('logo'):
            logo_path = f'static/images/{f}'
            break
    return render_template('settings.html', logo=logo_path)


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('error.html', error='Internal server error'), 500


@app.context_processor
def inject_logo():
    logo_path = None
    try:
        for f in os.listdir(IMG_DIR):
            if f.startswith('logo'):
                logo_path = os.path.join('static', 'images', f).replace('\\', '/')
                break
    except Exception:
        logo_path = None
    return dict(logo=logo_path)


# ==================== MAIN ====================
if __name__ == '__main__':
    init_database()
    
    print("\n" + "="*60)
    print("PHARMACY AUTOMATION SYSTEM")
    print("="*60)
    print(f"📁 Database: {DB_PATH}")
    print(f"🌐 Access: http://127.0.0.1:5000")
    print(f"📧 Admin: admin@pharma.local / admin123")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

