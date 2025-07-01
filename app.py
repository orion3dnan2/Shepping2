import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging (production-safe)
log_level = logging.INFO if os.environ.get('ENVIRONMENT') == 'production' else logging.DEBUG
logging.basicConfig(level=log_level)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)

# Security configurations
session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    if os.environ.get('ENVIRONMENT') == 'production':
        raise ValueError("SESSION_SECRET environment variable must be set for production security")
    else:
        # Development fallback - not secure for production
        import secrets
        session_secret = secrets.token_hex(32)
        logging.warning("Using auto-generated session secret for development. Set SESSION_SECRET environment variable for production.")

app.secret_key = session_secret
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # CSRF token expires in 1 hour
app.config['WTF_CSRF_SECRET_KEY'] = session_secret

# Initialize CSRF Protection
csrf = CSRFProtect(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# configure the database - PostgreSQL configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
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
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    
    db.create_all()
    
    # Create default super admin if it doesn't exist
    from models import Admin
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin', is_super_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        logging.info('Default super admin created: admin/admin123')
    elif not admin.is_super_admin:
        admin.is_super_admin = True
        db.session.commit()
        logging.info('Updated existing admin to super admin')

# Error handlers for production security
@app.errorhandler(404)
def page_not_found(e):
    from flask import render_template
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    from flask import render_template
    if os.environ.get('ENVIRONMENT') == 'production':
        # Hide error details in production
        return render_template('errors/500.html'), 500
    else:
        # Show error details in development
        import traceback
        return f"<h1>Internal Server Error</h1><pre>{traceback.format_exc()}</pre>", 500

@app.errorhandler(403)
def forbidden(e):
    from flask import render_template
    return render_template('errors/403.html'), 403

# Import routes after app initialization
import routes  # noqa: F401
