"""
Comprehensive seed script to add sample data for testing.
Run: python sample_seed.py
"""
from app import app, db
from app import User, Supplier, Customer, Medicine, Sale, Purchase
from datetime import date, timedelta


def seed():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Clear existing data
        db.session.query(Sale).delete()
        db.session.query(Purchase).delete()
        db.session.query(Medicine).delete()
        db.session.query(Customer).delete()
        db.session.query(Supplier).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # ========== Add Users ==========
        admin = User(name='Admin User', email='admin@pharmacy.com', role='admin')
        admin.set_password('admin123')
        
        staff = User(name='Staff Member', email='staff@pharmacy.com', role='staff')
        staff.set_password('staff123')
        
        customer1 = User(name='John Smith', email='john@example.com', role='customer')
        customer1.set_password('customer123')
        
        db.session.add_all([admin, staff, customer1])
        db.session.commit()
        print('✓ Added users')
        
        # ========== Add Suppliers ==========
        suppliers = [
            Supplier(
                name='HealthCare Global',
                email='sales@healthcareglobal.com',
                phone='+92-300-1234567',
                address='123 Medical Lane, Karachi'
            ),
            Supplier(
                name='MediSupply Pro',
                email='info@medisupply.com',
                phone='+92-300-2345678',
                address='456 Pharmacy Ave, Lahore'
            ),
            Supplier(
                name='PharmaMed Solutions',
                email='contact@pharmamed.com',
                phone='+92-300-3456789',
                address='789 Drug Street, Islamabad'
            ),
            Supplier(
                name='Vital Health Imports',
                email='vital@healthimports.com',
                phone='+92-300-4567890',
                address='321 Medicine Road, Multan'
            ),
            Supplier(
                name='Prime Pharmaceuticals',
                email='prime@pharma.com',
                phone='+92-300-5678901',
                address='654 Health Plaza, Peshawar'
            )
        ]
        db.session.add_all(suppliers)
        db.session.commit()
        print('✓ Added suppliers')
        
        # ========== Add Medicines ==========
        medicines_data = [
            # Painkillers
            ('Paracetamol 500mg', 'Painkiller', 45, 150, date.today() + timedelta(days=365), suppliers[0]),
            ('Ibuprofen 400mg', 'Painkiller', 55, 120, date.today() + timedelta(days=350), suppliers[1]),
            ('Aspirin 300mg', 'Painkiller', 30, 200, date.today() + timedelta(days=400), suppliers[2]),
            ('Naproxen 250mg', 'Painkiller', 75, 80, date.today() + timedelta(days=300), suppliers[3]),
            
            # Antibiotics
            ('Amoxicillin 500mg', 'Antibiotic', 120, 85, date.today() + timedelta(days=250), suppliers[0]),
            ('Azithromycin 250mg', 'Antibiotic', 180, 60, date.today() + timedelta(days=280), suppliers[1]),
            ('Ciprofloxacin 500mg', 'Antibiotic', 150, 70, date.today() + timedelta(days=320), suppliers[2]),
            ('Cephalexin 500mg', 'Antibiotic', 140, 95, date.today() + timedelta(days=260), suppliers[3]),
            
            # Vitamins & Supplements
            ('Vitamin D3 1000IU', 'Vitamin', 85, 200, date.today() + timedelta(days=450), suppliers[4]),
            ('Vitamin C 500mg', 'Vitamin', 60, 250, date.today() + timedelta(days=400), suppliers[0]),
            ('Multivitamin Tablet', 'Vitamin', 95, 180, date.today() + timedelta(days=380), suppliers[1]),
            ('Calcium + Vitamin D', 'Vitamin', 110, 140, date.today() + timedelta(days=420), suppliers[2]),
            
            # Antihistamines
            ('Cetirizine HCl 10mg', 'Antihistamine', 65, 110, date.today() + timedelta(days=350), suppliers[3]),
            ('Loratadine 10mg', 'Antihistamine', 70, 95, date.today() + timedelta(days=360), suppliers[4]),
            
            # Antacids
            ('Omeprazole 20mg', 'Antacid', 150, 130, date.today() + timedelta(days=300), suppliers[0]),
            ('Ranitidine HCl 150mg', 'Antacid', 85, 160, date.today() + timedelta(days=310), suppliers[1]),
            
            # Cough & Cold
            ('Cough Syrup', 'Cough/Cold', 45, 200, date.today() + timedelta(days=200), suppliers[2]),
            ('Decongestant Tablet', 'Cough/Cold', 55, 150, date.today() + timedelta(days=180), suppliers[3]),
            
            # Low Stock Items (for testing alerts)
            ('Insulin Injection', 'Diabetes', 500, 5, date.today() + timedelta(days=180), suppliers[4]),
            ('Heart Medication XYZ', 'Cardiac', 200, 8, date.today() + timedelta(days=150), suppliers[0]),
        ]
        
        medicines = []
        for name, category, price, qty, expiry, supplier in medicines_data:
            med = Medicine(
                name=name,
                category=category,
                price=price,
                quantity=qty,
                reorder_level=20,
                expiry_date=expiry,
                supplier_id=supplier.id
            )
            medicines.append(med)
        
        db.session.add_all(medicines)
        db.session.commit()
        print('✓ Added medicines')
        
        # ========== Add Customers ==========
        customers = [
            Customer(
                name='Ahmed Hassan',
                email='ahmed@example.com',
                phone='+92-300-1111111',
                address='123 Main Street, Karachi'
            ),
            Customer(
                name='Fatima Khan',
                email='fatima@example.com',
                phone='+92-300-2222222',
                address='456 Park Road, Lahore'
            ),
            Customer(
                name='Muhammad Ali',
                email='malik@example.com',
                phone='+92-300-3333333',
                address='789 Hill Street, Islamabad'
            ),
            Customer(
                name='Aisha Malik',
                email='aisha@example.com',
                phone='+92-300-4444444',
                address='321 Green Lane, Multan'
            ),
            Customer(
                name='Hassan Raza',
                email='hassan@example.com',
                phone='+92-300-5555555',
                address='654 Blue Avenue, Peshawar'
            ),
            Customer(
                name='Zainab Ahmed',
                email='zainab@example.com',
                phone='+92-300-6666666',
                address='987 Sunshine Road, Rawalpindi'
            ),
        ]
        db.session.add_all(customers)
        db.session.commit()
        print('✓ Added customers')
        
        # ========== Add Sales ==========
        sales = [
            Sale(customer_name='Ahmed Hassan', total=450.00, date=date.today() - timedelta(days=10)),
            Sale(customer_name='Fatima Khan', total=320.50, date=date.today() - timedelta(days=8)),
            Sale(customer_name='Muhammad Ali', total=675.75, date=date.today() - timedelta(days=5)),
            Sale(customer_name='Aisha Malik', total=540.25, date=date.today() - timedelta(days=3)),
            Sale(customer_name='Hassan Raza', total=890.00, date=date.today() - timedelta(days=2)),
            Sale(customer_name='Zainab Ahmed', total=230.50, date=date.today() - timedelta(days=1)),
            Sale(customer_name='Ahmed Hassan', total=420.75, date=date.today()),
        ]
        db.session.add_all(sales)
        db.session.commit()
        print('✓ Added sales')
        
        # ========== Add Purchases ==========
        purchases = [
            Purchase(supplier_id=suppliers[0].id, total=5000, date=date.today() - timedelta(days=15)),
            Purchase(supplier_id=suppliers[1].id, total=3500, date=date.today() - timedelta(days=12)),
            Purchase(supplier_id=suppliers[2].id, total=4200, date=date.today() - timedelta(days=8)),
            Purchase(supplier_id=suppliers[3].id, total=6000, date=date.today() - timedelta(days=5)),
            Purchase(supplier_id=suppliers[4].id, total=2800, date=date.today() - timedelta(days=2)),
        ]
        db.session.add_all(purchases)
        db.session.commit()
        print('✓ Added purchases')
        
        print('\n✅ Database seeding completed successfully!')
        print('\nTest Credentials:')
        print('  Admin: admin@pharmacy.com / admin123')
        print('  Staff: staff@pharmacy.com / staff123')
        print('  Customer: john@example.com / customer123')


if __name__ == '__main__':
    seed()
