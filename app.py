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

# configure the database - MySQL configuration for cPanel hosting
database_url = os.environ.get("DATABASE_URL")

# Multi-database configuration (PostgreSQL for Replit, MySQL for cPanel)
if database_url:
    # Handle PostgreSQL (current Replit environment)
    if database_url.startswith("postgres://") or database_url.startswith("postgresql://"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
            "echo": False,
        }
    # Handle MySQL (cPanel hosting)
    elif database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
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
    elif database_url.startswith("mysql+pymysql://"):
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
    else:
        # Default configuration
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
            "echo": False,
        }
else:
    # Default cPanel MySQL connection format for documentation
    database_url = "mysql+pymysql://username:password@localhost/database_name"
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

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
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
        
        # Create all database tables
        db.create_all()
        logging.info('Database tables created/verified successfully')
        
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
        logging.error(f'Database initialization error: {str(e)}')
        # Don't crash the app, let it start without database for debugging
        pass

# Import routes after app initialization
import routes  # noqa: F401
