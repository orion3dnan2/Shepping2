import os
import logging
from datetime import timedelta

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
if not database_url:
    # Default MySQL configuration for development
    database_url = "mysql+pymysql://root:password123@localhost:3306/shipping_db"
    print("INFO: Using default MySQL configuration for development")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

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
        
        # Only initialize if we have a proper MySQL connection
        if app.config["SQLALCHEMY_DATABASE_URI"] and "mysql" in app.config["SQLALCHEMY_DATABASE_URI"]:
            # Create all database tables
            db.create_all()
            logging.info('MySQL database tables created/verified successfully')
            
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
        else:
            logging.warning('MySQL database not configured. Please set DATABASE_URL with MySQL connection string.')
            
    except Exception as e:
        logging.error(f'Database initialization error: {str(e)}')
        logging.info('Application configured for MySQL. Please ensure MySQL server is running and DATABASE_URL is set correctly.')
        # Don't crash the app, let it start without database for debugging
        pass

# Import routes after app initialization
import routes  # noqa: F401
