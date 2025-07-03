import os
import logging
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shipment.db"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Simple route to indicate the system has been migrated
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Shipment Management System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .info { background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .php-link { background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }
            .php-link:hover { background: #45a049; }
            .arabic { direction: rtl; font-family: 'Tahoma', Arial, sans-serif; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Shipment Management System</h1>
            <div class="info">
                <h2>System Migration Notice</h2>
                <p>This system has been successfully migrated to PHP for improved deployment compatibility.</p>
                <p class="arabic">تم ترحيل النظام بنجاح إلى PHP لتحسين التوافق مع خدمات الاستضافة.</p>
            </div>
            
            <h3>Access Options:</h3>
            <p>
                <a href="/php_version/" class="php-link">🚀 Access PHP Version</a>
            </p>
            
            <div class="info">
                <h3>Migration Benefits:</h3>
                <ul>
                    <li>✅ Simplified deployment process</li>
                    <li>✅ Better hosting compatibility</li>
                    <li>✅ Reduced server requirements</li>
                    <li>✅ Faster deployment times</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/php_version/')
def php_redirect():
    return redirect('/php_version/index.php')

# Error handler
@app.errorhandler(404)
def not_found(error):
    return """
    <html>
    <head>
        <title>Page Not Found</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <p><a href="/">← Return to Home</a></p>
        </div>
    </body>
    </html>
    """, 404

with app.app_context():
    try:
        db.create_all()
        app.logger.info("Database tables created successfully")
    except Exception as e:
        app.logger.error(f"Error creating database tables: {e}")