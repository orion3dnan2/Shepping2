"""
cPanel Configuration Helper
This script helps configure the application for cPanel hosting
"""

import os
import sys
from pathlib import Path

# cPanel specific configurations
CPANEL_CONFIG = {
    'python_version': '3.11',
    'app_root': '/home/username/public_html',
    'passenger_wsgi': 'passenger_wsgi.py',
    'virtual_env': '/home/username/virtualenv/public_html/3.11',
    'requirements_file': 'requirements_cpanel.txt'
}

# Database configuration template
DATABASE_CONFIG_TEMPLATE = {
    'host': 'localhost',
    'port': '3306',
    'charset': 'utf8mb4',
    'driver': 'pymysql',
    'url_format': 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
}

# Required environment variables for cPanel
REQUIRED_ENV_VARS = [
    'DATABASE_URL',
    'SESSION_SECRET',
    'FLASK_ENV'
]

# cPanel .htaccess template
HTACCESS_TEMPLATE = """# cPanel Flask Application Configuration
PassengerEnabled on
PassengerAppRoot {app_root}
PassengerPython {python_path}
PassengerStartupFile {startup_file}

# Environment Variables
SetEnv SESSION_SECRET "{session_secret}"
SetEnv FLASK_ENV "production"
SetEnv DATABASE_URL "{database_url}"

# Static Files Configuration
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 month"
    Header set Cache-Control "public, max-age=2592000"
</FilesMatch>

# Security Settings
<Files "*.py">
    Order allow,deny
    Deny from all
</Files>

<Files "*.pyc">
    Order allow,deny
    Deny from all
</Files>

<Files "requirements*.txt">
    Order allow,deny
    Deny from all
</Files>

<Files "*.log">
    Order allow,deny
    Deny from all
</Files>

<Files ".env">
    Order allow,deny
    Deny from all
</Files>

# Arabic Language Support
AddDefaultCharset UTF-8
"""

def generate_htaccess(username, database_details, session_secret):
    """Generate .htaccess file for cPanel"""
    config = CPANEL_CONFIG.copy()
    config['app_root'] = f'/home/{username}/public_html'
    config['python_path'] = f'/home/{username}/virtualenv/public_html/3.11/bin/python'
    config['startup_file'] = 'passenger_wsgi.py'
    
    database_url = DATABASE_CONFIG_TEMPLATE['url_format'].format(
        username=database_details['username'],
        password=database_details['password'],
        host=database_details.get('host', 'localhost'),
        port=database_details.get('port', '3306'),
        database=database_details['database']
    )
    
    return HTACCESS_TEMPLATE.format(
        app_root=config['app_root'],
        python_path=config['python_path'],
        startup_file=config['startup_file'],
        session_secret=session_secret,
        database_url=database_url
    )

def check_cpanel_requirements():
    """Check if the application is ready for cPanel deployment"""
    issues = []
    
    # Check required files
    required_files = [
        'passenger_wsgi.py',
        'requirements_cpanel.txt',
        'app.py',
        'main.py',
        'models.py',
        'routes.py'
    ]
    
    for file in required_files:
        if not Path(file).exists():
            issues.append(f"Missing file: {file}")
    
    # Check if templates and static directories exist
    if not Path('templates').exists():
        issues.append("Missing templates directory")
    
    if not Path('static').exists():
        issues.append("Missing static directory")
    
    return issues

if __name__ == "__main__":
    print("=== cPanel Configuration Helper ===")
    
    # Check requirements
    issues = check_cpanel_requirements()
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  ✗ {issue}")
        sys.exit(1)
    
    print("✓ All required files are present")
    print("✓ Ready for cPanel deployment")
    print("\nNext steps:")
    print("1. Upload all files to cPanel public_html")
    print("2. Create MySQL database and user")
    print("3. Update .htaccess with your database credentials")
    print("4. Install Python packages in virtual environment")
    print("5. Run app_start.py to initialize database")