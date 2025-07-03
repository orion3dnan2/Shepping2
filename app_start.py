#!/usr/bin/env python3
"""
Application starter for cPanel hosting
This file can be used to initialize the application and database
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def setup_database():
    """Initialize database tables and create admin user if needed"""
    from app import app, db
    from models import Admin
    
    try:
        with app.app_context():
            # Create all database tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Check if admin user exists
            admin = Admin.query.filter_by(username='admin').first()
            if not admin:
                # Create default admin user
                admin = Admin(username='admin', is_super_admin=True)
                admin.set_password('admin123')  # Change this password!
                admin.set_permissions({
                    'home': True,
                    'shipments': True,
                    'tracking': True,
                    'reports': True,
                    'expenses': True,
                    'add_shipment': True,
                    'settings': True
                })
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created (username: admin, password: admin123)")
                print("⚠️  IMPORTANT: Change the admin password after first login!")
            else:
                print("✓ Admin user already exists")
                
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return False
    
    return True

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_login', 'flask_migrate',
        'pymysql', 'sqlalchemy', 'werkzeug', 'jinja2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"✗ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements_cpanel.txt")
        return False
    
    print("✓ All required packages are installed")
    return True

if __name__ == "__main__":
    print("=== cPanel Flask Application Setup ===")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    print("\n=== Setup Complete ===")
    print("Your application is ready for cPanel deployment!")
    print("Access URL: https://yourdomain.com")
    print("Admin Login: admin / admin123")
    print("Don't forget to change the admin password!")