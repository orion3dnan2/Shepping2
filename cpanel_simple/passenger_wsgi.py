#!/usr/bin/env python3
"""
WSGI Configuration for cPanel Hosting
Shipping Management System - cPanel Deployment
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set environment variables for cPanel
os.environ.setdefault('FLASK_ENV', 'production')

try:
    # Import the Flask application
    from app import app as application
    
    # Ensure proper configuration for cPanel
    if __name__ == "__main__":
        application.run(debug=False, host='0.0.0.0', port=5000)
        
except ImportError as e:
    # Create a simple WSGI application for debugging
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        
        error_message = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>خطأ في التكوين</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; padding: 20px; }}
                .error {{ background: #f8d7da; padding: 20px; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>خطأ في تحميل التطبيق</h2>
                <p>تفاصيل الخطأ: {str(e)}</p>
                <p>تأكد من:</p>
                <ul>
                    <li>تم رفع جميع ملفات Python (.py)</li>
                    <li>تم تثبيت المكتبات المطلوبة</li>
                    <li>تم تكوين قاعدة البيانات بشكل صحيح</li>
                </ul>
            </div>
        </body>
        </html>
        """.encode('utf-8')
        
        return [error_message]