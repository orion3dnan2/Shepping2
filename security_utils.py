"""
Security utility functions for input validation and sanitization
"""
import re
import bleach
from functools import wraps
from flask import request, abort, session, current_app
from flask_login import current_user
from datetime import datetime, timedelta

# Allowed HTML tags and attributes for sanitization
ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

def sanitize_input(text):
    """Sanitize user input to prevent XSS attacks"""
    if not text:
        return text
    
    # Remove any HTML tags and scripts
    cleaned = bleach.clean(str(text), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    
    # Additional cleaning for common injection patterns
    cleaned = re.sub(r'<script[^>]*>.*?</script>', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'on\w+\s*=', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()

def validate_phone_number(phone):
    """Validate phone number format"""
    if not phone:
        return True  # Allow empty phone numbers
    
    # Allow numbers, spaces, hyphens, parentheses, and plus sign
    pattern = r'^[\+]?[\d\s\-\(\)]+$'
    return bool(re.match(pattern, phone)) and len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')) >= 8

def validate_email(email):
    """Validate email format"""
    if not email:
        return True  # Allow empty emails
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_tracking_number(tracking_number):
    """Validate tracking number format"""
    if not tracking_number:
        return False
    
    # Expected format: SHIP-YYYYMMDD-XXX
    pattern = r'^SHIP-\d{8}-\d{3}$'
    return bool(re.match(pattern, tracking_number))

def validate_decimal(value, min_val=0, max_val=None):
    """Validate decimal/float values"""
    try:
        float_val = float(value)
        if float_val < min_val:
            return False
        if max_val is not None and float_val > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_required_fields(data, required_fields):
    """Validate that required fields are present and not empty"""
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            return False, f"الحقل {field} مطلوب"
    return True, None

def check_session_timeout():
    """Check if session has timed out"""
    if 'last_activity' in session:
        last_activity = datetime.fromisoformat(session['last_activity'])
        if datetime.now() - last_activity > current_app.permanent_session_lifetime:
            return True
    return False

def update_session_activity():
    """Update last activity time in session"""
    session['last_activity'] = datetime.now().isoformat()
    session.permanent = True

def require_admin_permission(permission):
    """Decorator to require specific admin permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            if not current_user.has_permission(permission):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_super_admin(f):
    """Decorator to require super admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        
        if not current_user.is_super_admin:
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def validate_file_upload(file):
    """Validate uploaded files for security"""
    if not file:
        return False, "لم يتم اختيار ملف"
    
    # Check file size (max 5MB)
    if len(file.read()) > 5 * 1024 * 1024:
        return False, "حجم الملف كبير جداً (الحد الأقصى 5 ميجابايت)"
    
    file.seek(0)  # Reset file pointer
    
    # Check file extension
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.txt'}
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return False, "نوع الملف غير مسموح"
    
    return True, None

def prevent_directory_traversal(path):
    """Prevent directory traversal attacks"""
    # Remove any path traversal attempts
    clean_path = path.replace('..', '').replace('/', '').replace('\\', '')
    
    # Only allow alphanumeric characters, hyphens, underscores, and dots
    pattern = r'^[a-zA-Z0-9._-]+$'
    if not re.match(pattern, clean_path):
        return None
    
    return clean_path

def rate_limit_check(identifier, max_requests=100, window_minutes=15):
    """Basic rate limiting implementation"""
    # This would typically use Redis or database for persistence
    # For now, using session storage as a simple implementation
    rate_limit_key = f"rate_limit_{identifier}"
    current_time = datetime.now()
    
    if rate_limit_key in session:
        requests_data = session[rate_limit_key]
        # Clean old requests outside the window
        requests_data = [req_time for req_time in requests_data 
                        if current_time - datetime.fromisoformat(req_time) < timedelta(minutes=window_minutes)]
        
        if len(requests_data) >= max_requests:
            return False
        
        requests_data.append(current_time.isoformat())
        session[rate_limit_key] = requests_data
    else:
        session[rate_limit_key] = [current_time.isoformat()]
    
    return True

def log_security_event(event_type, user_id=None, ip_address=None, details=None):
    """Log security-related events"""
    import logging
    
    logger = logging.getLogger('security')
    
    log_data = {
        'event': event_type,
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id or (current_user.id if current_user.is_authenticated else None),
        'ip_address': ip_address or request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'details': details
    }
    
    logger.warning(f"Security Event: {log_data}")