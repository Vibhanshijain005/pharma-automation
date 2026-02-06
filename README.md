# Pharmacy Automation System

This is a simple Pharmacy Automation System built with Flask, SQLite, and Bootstrap. It is intended as a college final-year project starter template: functional, beginner-friendly, and easy to extend.

Features
- User registration and login (Admin, Pharmacist, Customer)
- Dashboard with statistics
- Medicine CRUD with expiry and low-stock awareness
- Billing with invoice PDF generation
- Customers and Suppliers management
- Sales records and simple reports
- Responsive UI with Bootstrap and dark mode toggle

Quick install
1. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.

Default admin
- Email: admin@pharma.local
- Password: admin123

Database
- Using SQLite at `database/pharmacy.db` (created automatically)
- Schema reference: `database/schema.sql`
- Optional: run `python sample_seed.py` to add sample suppliers, medicines and a customer

Notes
- Passwords are hashed using Werkzeug.
- Invoice PDF is generated with ReportLab and downloaded immediately after billing.
- For production change `SECRET_KEY` and use a production-ready database (MySQL/Postgres).

Extending the project
- Add email notifications using `flask-mail` or an external service.
- Add better forms and validation with `Flask-WTF`.
- Add role management pages (promote/demote users).

Files
- `app.py`: main Flask application routes and logic
- `models/models.py`: SQLAlchemy models
- `templates/`: Jinja2 HTML templates
- `static/`: CSS and JS assets
- `database/schema.sql`: SQL schema for reference
