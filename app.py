import os
import logging
from datetime import timedelta

from flask import Flask, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging - disable debug in production
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# Security configurations
app.config['SESSION_COOKIE_SECURE'] = True if os.environ.get('FLASK_ENV') == 'production' else False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 30 minute session timeout
app.config['WTF_CSRF_TIME_LIMIT'] = None  # CSRF tokens don't expire

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # XSS Protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com cdn.jsdelivr.net fonts.googleapis.com; "
        "font-src 'self' fonts.gstatic.com; "
        "img-src 'self' data: *.tile.openstreetmap.org; "
        "connect-src 'self';"
    )
    
    # Strict Transport Security (HTTPS only)
    if app.config.get('SESSION_COOKIE_SECURE'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

# Session management and security middleware
@app.before_request
def before_request():
    from security_utils import check_session_timeout, update_session_activity, log_security_event
    from flask_login import current_user, logout_user
    from flask import session, request, redirect, url_for
    
    # Check for session timeout
    if current_user.is_authenticated and check_session_timeout():
        logout_user()
        session.clear()
        log_security_event('session_timeout', user_id=current_user.id)
        return redirect(url_for('login'))
    
    # Update session activity
    if current_user.is_authenticated:
        update_session_activity()
    
    # Log suspicious requests
    if len(request.args) > 50:  # Too many parameters
        log_security_event('suspicious_request', details=f'Too many parameters: {len(request.args)}')
    
    # Check for common attack patterns in URL
    suspicious_patterns = ['../', '<script', 'javascript:', 'eval(', 'union select']
    url = request.url.lower()
    for pattern in suspicious_patterns:
        if pattern in url:
            log_security_event('suspicious_request', details=f'Attack pattern detected: {pattern}')
            abort(400)

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

# Import routes after app initialization
import routes  # noqa: F401
