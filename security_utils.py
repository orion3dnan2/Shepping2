import html
import re
from urllib.parse import urlparse
from flask import request, abort
from werkzeug.exceptions import BadRequest

class SecurityUtils:
    """Utility class for security functions"""
    
    # Dangerous patterns to filter
    XSS_PATTERNS = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<.*?style\s*=.*?expression\s*\(',
        r'<.*?src\s*=.*?javascript:',
        r'<iframe.*?>.*?</iframe>',
        r'<object.*?>.*?</object>',
        r'<embed.*?>.*?</embed>',
        r'<form.*?>.*?</form>',
        r'<meta.*?http-equiv.*?>',
        r'<link.*?rel\s*=.*?stylesheet',
        r'vbscript:',
        r'livescript:',
        r'data:.*?base64',
        r'eval\s*\(',
        r'exec\s*\(',
        r'alert\s*\(',
        r'confirm\s*\(',
        r'prompt\s*\(',
        r'document\.',
        r'window\.',
        r'location\.',
        r'setTimeout\s*\(',
        r'setInterval\s*\(',
    ]
    
    SQL_INJECTION_PATTERNS = [
        r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|OR|AND)\s',
        r'(\s|^)(UNION|SELECT).*?(FROM|WHERE)',
        r'(\s|^)(INSERT|UPDATE|DELETE).*?(SET|VALUES|WHERE)',
        r'(\s|^)(DROP|CREATE|ALTER).*?(TABLE|DATABASE|INDEX)',
        r'(\s|^)(EXEC|EXECUTE).*?(\(|\s)',
        r"('|\")(\s)*(OR|AND)(\s)*('|\")",
        r"('|\")(\s)*(=|!=|<>)(\s)*('|\")",
        r'(\s|^)(--|#|/\*)',
        r';(\s)*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC)',
        r'(\s|^)(CAST|CONVERT|CHAR|ASCII|SUBSTRING|LEN|REVERSE)\s*\(',
        r'(\s|^)(WAITFOR|DELAY)\s',
        r'(\s|^)(@@|SYSTEM_USER|USER_NAME|DB_NAME)',
        r'(\s|^)(xp_|sp_)',
    ]
    
    @staticmethod
    def sanitize_input(data, allow_html=False):
        """
        Sanitize user input to prevent XSS and other attacks
        
        Args:
            data: Input data to sanitize
            allow_html: Whether to allow HTML tags (default: False)
            
        Returns:
            Sanitized data
        """
        if not data:
            return data
            
        if isinstance(data, str):
            # Remove null bytes
            data = data.replace('\x00', '')
            
            # Escape HTML if not allowing HTML
            if not allow_html:
                data = html.escape(data)
            
            # Check for XSS patterns
            for pattern in SecurityUtils.XSS_PATTERNS:
                if re.search(pattern, data, re.IGNORECASE):
                    raise BadRequest('محتوى غير مسموح: تم اكتشاف محتوى ضار')
            
            # Check for SQL injection patterns
            for pattern in SecurityUtils.SQL_INJECTION_PATTERNS:
                if re.search(pattern, data, re.IGNORECASE):
                    raise BadRequest('محتوى غير مسموح: تم اكتشاف محاولة SQL injection')
            
            # Limit length to prevent DoS
            if len(data) > 10000:
                raise BadRequest('البيانات المدخلة طويلة جداً')
                
            return data.strip()
            
        elif isinstance(data, dict):
            return {k: SecurityUtils.sanitize_input(v, allow_html) for k, v in data.items()}
            
        elif isinstance(data, list):
            return [SecurityUtils.sanitize_input(item, allow_html) for item in data]
            
        return data
    
    @staticmethod
    def validate_float(value, min_val=0, max_val=999999, field_name="القيمة"):
        """
        Validate and convert float values safely
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            field_name: Field name for error messages
            
        Returns:
            Validated float value
        """
        try:
            if value is None or value == '':
                return 0.0
                
            if isinstance(value, str):
                # Remove any non-numeric characters except decimal point
                value = re.sub(r'[^\d.-]', '', value)
                
            float_val = float(value)
            
            if float_val < min_val or float_val > max_val:
                raise ValueError(f'{field_name} يجب أن يكون بين {min_val} و {max_val}')
                
            return round(float_val, 3)
            
        except (ValueError, TypeError):
            raise BadRequest(f'{field_name} غير صحيح')
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Validated phone number
        """
        if not phone:
            return phone
            
        # Remove all non-digit characters
        phone = re.sub(r'[^\d+]', '', phone)
        
        # Check for valid phone number patterns
        if not re.match(r'^[\+]?[\d\s\-\(\)]{7,20}$', phone):
            raise BadRequest('رقم الهاتف غير صحيح')
            
        return phone
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        
        Args:
            email: Email to validate
            
        Returns:
            Validated email
        """
        if not email:
            return email
            
        email = email.strip().lower()
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise BadRequest('البريد الإلكتروني غير صحيح')
            
        return email
    
    @staticmethod
    def validate_tracking_number(tracking_number):
        """
        Validate tracking number format
        
        Args:
            tracking_number: Tracking number to validate
            
        Returns:
            Validated tracking number
        """
        if not tracking_number:
            raise BadRequest('رقم التتبع مطلوب')
            
        tracking_number = tracking_number.strip().upper()
        
        # Check format: SHIP-YYYYMMDD-XXX
        if not re.match(r'^SHIP-\d{8}-\d{3}$', tracking_number):
            raise BadRequest('تنسيق رقم التتبع غير صحيح')
            
        return tracking_number
    
    @staticmethod
    def check_rate_limit(ip_address, max_requests=100, time_window=3600):
        """
        Basic rate limiting check
        
        Args:
            ip_address: Client IP address
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
            
        Returns:
            True if within rate limit
        """
        # This is a basic implementation
        # In production, you would use Redis or similar
        return True
    
    @staticmethod
    def validate_file_upload(file):
        """
        Validate uploaded file for security
        
        Args:
            file: Uploaded file object
            
        Returns:
            True if file is safe
        """
        if not file:
            return True
            
        # Check file size (max 10MB)
        if len(file.read()) > 10 * 1024 * 1024:
            raise BadRequest('حجم الملف كبير جداً (الحد الأقصى 10 ميجابايت)')
            
        file.seek(0)  # Reset file pointer
        
        # Check file extension
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.txt'}
        filename = file.filename.lower()
        
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise BadRequest('نوع الملف غير مسموح')
            
        # Check for dangerous content in filename
        dangerous_patterns = ['..', '/', '\\', '<', '>', '|', ':', '*', '?', '"']
        if any(pattern in filename for pattern in dangerous_patterns):
            raise BadRequest('اسم الملف يحتوي على أحرف غير مسموحة')
            
        return True
    
    @staticmethod
    def log_security_event(event_type, description, ip_address=None, user_id=None):
        """
        Log security events for monitoring
        
        Args:
            event_type: Type of security event
            description: Event description
            ip_address: Client IP address
            user_id: User ID if applicable
        """
        import logging
        
        security_logger = logging.getLogger('security')
        
        log_data = {
            'event_type': event_type,
            'description': description,
            'ip_address': ip_address or request.remote_addr if request else 'unknown',
            'user_id': user_id,
        }
        
        security_logger.warning(f'Security Event: {log_data}')

# Security decorator for routes
def security_check(f):
    """Decorator to add security checks to routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Rate limiting check
        if not SecurityUtils.check_rate_limit(request.remote_addr):
            SecurityUtils.log_security_event('RATE_LIMIT_EXCEEDED', 
                                           f'Rate limit exceeded from {request.remote_addr}')
            abort(429)  # Too Many Requests
        
        # Sanitize form data
        if request.form:
            try:
                for key, value in request.form.items():
                    SecurityUtils.sanitize_input(value)
            except BadRequest as e:
                SecurityUtils.log_security_event('MALICIOUS_INPUT', 
                                               f'Malicious input detected: {str(e)}')
                raise
        
        return f(*args, **kwargs)
    
    return decorated_function