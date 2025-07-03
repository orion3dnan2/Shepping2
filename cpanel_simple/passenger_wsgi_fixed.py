#!/usr/bin/env python3
"""
Enhanced WSGI Configuration for cPanel Hosting
Fixes common 503 errors and improves error handling
"""

import sys
import os
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set default environment variables
os.environ.setdefault('FLASK_ENV', 'production')

def create_error_application(error_msg):
    """Create a fallback WSGI application for error display"""
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        
        error_html = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>خطأ في النظام</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    direction: rtl; 
                    padding: 20px; 
                    background: #f5f5f5;
                    margin: 0;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .error {{ 
                    background: #f8d7da; 
                    padding: 20px; 
                    border-radius: 8px; 
                    border: 1px solid #f5c6cb;
                    margin-bottom: 20px;
                }}
                .info {{
                    background: #d4edda;
                    padding: 15px;
                    border-radius: 5px;
                    border: 1px solid #c3e6cb;
                }}
                h2 {{ color: #721c24; }}
                .steps {{ margin-top: 20px; }}
                .steps li {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error">
                    <h2>⚠️ خطأ في تحميل نظام إدارة الشحن</h2>
                    <p><strong>تفاصيل الخطأ:</strong> {error_msg}</p>
                </div>
                
                <div class="info">
                    <h3>خطوات حل المشكلة:</h3>
                    <div class="steps">
                        <ol>
                            <li><strong>تحقق من ملفات Python:</strong> تأكد من رفع جميع ملفات .py</li>
                            <li><strong>المكتبات المطلوبة:</strong> قم بتشغيل: pip install -r requirements_cpanel.txt</li>
                            <li><strong>قاعدة البيانات:</strong> تحقق من معلومات الاتصال في .htaccess</li>
                            <li><strong>مسار Python:</strong> تأكد من صحة PassengerPython في .htaccess</li>
                            <li><strong>الأذونات:</strong> تأكد من أذونات الملفات (644 للملفات، 755 للمجلدات)</li>
                        </ol>
                    </div>
                </div>
                
                <p><small>نظام إدارة الشحن - إصدار الإنتاج</small></p>
            </div>
        </body>
        </html>
        """.encode('utf-8')
        
        return [error_html]
    
    return application

try:
    # Attempt to import the Flask application
    logger.info("Attempting to import Flask application...")
    from app import app as application
    logger.info("Flask application imported successfully")
    
    # Test if the app can be initialized
    with application.app_context():
        logger.info("Flask application context initialized successfully")
    
except ImportError as e:
    logger.error(f"ImportError: {e}")
    application = create_error_application(f"خطأ في استيراد الوحدات: {str(e)}")
    
except Exception as e:
    logger.error(f"General error: {e}")
    application = create_error_application(f"خطأ عام: {str(e)}")

# For debugging purposes
if __name__ == "__main__":
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error running application: {e}")