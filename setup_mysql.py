#!/usr/bin/env python3
"""
MySQL Database Setup Script for cPanel Hosting
Shipping Management System - Database Initialization
"""

import os
import sys
from datetime import datetime

def check_mysql_connection():
    """Test MySQL connection and create tables"""
    try:
        import pymysql
        print("✓ PyMySQL library found")
        
        # Get database configuration from environment
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL environment variable not found")
            print("Please set DATABASE_URL in your .htaccess file")
            return False
            
        # Parse MySQL connection string
        if database_url.startswith("mysql+pymysql://"):
            # Remove mysql+pymysql:// prefix
            conn_str = database_url[17:]
            
            # Parse user:password@host/database
            auth_part, host_db = conn_str.split('@')
            username, password = auth_part.split(':')
            host, database = host_db.split('/')
            
            print(f"Connecting to MySQL: {username}@{host}/{database}")
            
            # Test connection
            connection = pymysql.connect(
                host=host,
                user=username,
                password=password,
                database=database,
                charset='utf8mb4'
            )
            
            print("✓ MySQL connection successful")
            connection.close()
            return True
            
    except ImportError:
        print("❌ PyMySQL library not found")
        print("Install with: pip install pymysql")
        return False
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        return False

def create_admin_user():
    """Create default admin user"""
    try:
        # Import Flask app
        sys.path.insert(0, os.path.dirname(__file__))
        from app import app, db
        from models import Admin
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✓ Database tables created")
            
            # Check if admin user exists
            admin = Admin.query.filter_by(username='admin').first()
            if not admin:
                # Create default admin
                from werkzeug.security import generate_password_hash
                
                admin = Admin(
                    username='admin',
                    email='admin@shipping.com',
                    password_hash=generate_password_hash('admin123'),
                    is_super_admin=True,
                    permissions={
                        'home': True,
                        'shipments': True,
                        'tracking': True,
                        'reports': True,
                        'expenses': True,
                        'add_shipment': True,
                        'settings': True
                    }
                )
                
                db.session.add(admin)
                db.session.commit()
                print("✓ Default admin user created (admin/admin123)")
            else:
                print("✓ Admin user already exists")
                
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("🚢 Shipping Management System")
    print("MySQL Database Setup for cPanel")
    print("=" * 50)
    print()
    
    # Check MySQL connection
    print("1. Testing MySQL connection...")
    if not check_mysql_connection():
        sys.exit(1)
    print()
    
    # Create database tables and admin user
    print("2. Setting up database tables...")
    if not create_admin_user():
        sys.exit(1)
    print()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print()
    print("🔑 Default Login Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print()
    print("⚠️  IMPORTANT: Change the default password after first login!")
    print("=" * 50)

if __name__ == "__main__":
    main()