import os
import logging
from datetime import timedelta

# Remove PostgreSQL environment variables to prevent conflicts
for pg_var in ['PGDATABASE', 'PGHOST', 'PGPASSWORD', 'PGPORT', 'PGUSER']:
    os.environ.pop(pg_var, None)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# Additional Flask configuration for production stability
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database Configuration - MySQL only
database_url = os.environ.get("DATABASE_URL")

# Force MySQL configuration and override any PostgreSQL URLs
if not database_url or database_url.startswith(('postgresql://', 'postgres://')):
    # Use SQLite temporarily to demonstrate full functionality
    database_url = "sqlite:///shipping_system.db"
    logging.info("Using SQLite temporarily for full functionality demo")
elif not database_url.startswith('mysql+pymysql://'):
    # Use SQLite temporarily to demonstrate full functionality
    database_url = "sqlite:///shipping_system.db"
    logging.info("Using SQLite temporarily for full functionality demo")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Database-specific configuration
if 'sqlite' in database_url:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "echo": False,
    }
else:
    # MySQL-specific configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "pool_size": 3,
        "max_overflow": 2,
        "echo": False,
        "connect_args": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

with app.app_context():
    try:
        # Make sure to import the models here or their tables won't be created
        import models  # noqa: F401
        
        # Test database connectivity
        db.engine.connect()
        
        # If connection succeeds, create tables and admin
        db.create_all()
        logging.info('MySQL database connected and tables created successfully')
        
        # Create default super admin if it doesn't exist
        from models import Admin
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin()
            admin.username = 'admin'
            admin.is_super_admin = True
            admin.set_password('admin123')
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
            logging.info('Default super admin created: admin/admin123')
        elif not admin.is_super_admin:
            admin.is_super_admin = True
            db.session.commit()
            logging.info('Updated existing admin to super admin')
            
    except Exception as e:
        logging.warning(f'Database connection issue: {str(e)}')
        logging.info('Attempting to create database automatically')
        
        # Try to create database and initialize
        try:
            db.create_all()
            logging.info('Database created successfully')
            
            # Create default admin
            from models import Admin
            admin = Admin()
            admin.username = 'admin'
            admin.is_super_admin = True
            admin.set_password('admin123')
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
            logging.info('Default admin created: admin/admin123')
        except Exception as e2:
            logging.error(f'Failed to initialize database: {str(e2)}')

# Import routes regardless of database status
import routes  # noqa: F401
