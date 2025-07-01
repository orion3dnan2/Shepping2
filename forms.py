"""
Secure forms with CSRF protection and input validation for Morsal Express System
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, TextAreaField, BooleanField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, Regexp, EqualTo
from wtforms.widgets import HiddenInput
import re


class LoginForm(FlaskForm):
    """Secure login form with CSRF protection"""
    username = StringField('اسم المستخدم', validators=[
        DataRequired(message='اسم المستخدم مطلوب'),
        Length(min=3, max=80, message='اسم المستخدم يجب أن يكون بين 3 و 80 حرف'),
        Regexp(r'^[a-zA-Z0-9_]+$', message='اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة'),
        Length(min=8, message='كلمة المرور يجب أن تحتوي على 8 أحرف على الأقل')
    ])


class AddShipmentForm(FlaskForm):
    """Secure shipment creation form with comprehensive validation"""
    # Sender information
    sender_name = StringField('اسم المرسل', validators=[
        DataRequired(message='اسم المرسل مطلوب'),
        Length(min=2, max=100, message='اسم المرسل يجب أن يكون بين 2 و 100 حرف')
    ])
    sender_phone = StringField('هاتف المرسل', validators=[
        DataRequired(message='هاتف المرسل مطلوب'),
        Regexp(r'^[\d\s\+\-\(\)]+$', message='رقم الهاتف غير صحيح')
    ])
    sender_address = TextAreaField('عنوان المرسل', validators=[
        Optional(),
        Length(max=200, message='العنوان طويل جداً')
    ])
    sender_email = StringField('إيميل المرسل', validators=[
        Optional(),
        Email(message='صيغة الإيميل غير صحيحة')
    ])
    
    # Receiver information
    receiver_name = StringField('اسم المستلم', validators=[
        DataRequired(message='اسم المستلم مطلوب'),
        Length(min=2, max=100, message='اسم المستلم يجب أن يكون بين 2 و 100 حرف')
    ])
    receiver_phone = StringField('هاتف المستلم', validators=[
        DataRequired(message='هاتف المستلم مطلوب'),
        Regexp(r'^[\d\s\+\-\(\)]+$', message='رقم الهاتف غير صحيح')
    ])
    receiver_address = TextAreaField('عنوان المستلم', validators=[
        Optional(),
        Length(max=200, message='العنوان طويل جداً')
    ])
    receiver_email = StringField('إيميل المستلم', validators=[
        Optional(),
        Email(message='صيغة الإيميل غير صحيحة')
    ])
    
    # Shipment details
    direction = SelectField('اتجاه الشحن', choices=[
        ('kuwait_to_sudan', 'الكويت إلى السودان'),
        ('sudan_to_kuwait', 'السودان إلى الكويت')
    ], validators=[DataRequired(message='اتجاه الشحن مطلوب')])
    
    package_type = SelectField('نوع الشحنة', validators=[
        DataRequired(message='نوع الشحنة مطلوب')
    ])
    
    shipping_method = SelectField('طريق الشحن', choices=[
        ('جوي', 'جوي'),
        ('بري', 'بري')
    ], validators=[Optional()])
    
    document_type = SelectField('نوع المستند', validators=[Optional()])
    
    package_contents = TextAreaField('محتويات الشحنة', validators=[
        Optional(),
        Length(max=200, message='وصف المحتويات طويل جداً')
    ])
    
    weight = DecimalField('الوزن (كيلوغرام)', validators=[
        Optional(),
        NumberRange(min=0.001, max=1000, message='الوزن يجب أن يكون بين 0.001 و 1000 كيلوغرام')
    ], places=3)
    
    zone = StringField('المنطقة', validators=[
        Optional(),
        Length(max=50, message='اسم المنطقة طويل جداً')
    ])
    
    price = DecimalField('السعر الإجمالي', validators=[
        DataRequired(message='السعر مطلوب'),
        NumberRange(min=0, message='السعر يجب أن يكون أكبر من الصفر')
    ], places=3)
    
    paid_amount = DecimalField('المبلغ المدفوع', validators=[
        Optional(),
        NumberRange(min=0, message='المبلغ المدفوع يجب أن يكون أكبر من أو يساوي الصفر')
    ], places=3)
    
    # Checkboxes
    has_packaging = BooleanField('تغليف')
    has_policy = BooleanField('سياسة')
    has_comment = BooleanField('تعليق')
    
    waybill_price = DecimalField('سعر بوليصة الشحن', validators=[
        Optional(),
        NumberRange(min=0, message='سعر البوليصة يجب أن يكون أكبر من أو يساوي الصفر')
    ], places=3)
    
    notes = TextAreaField('ملاحظات', validators=[
        Optional(),
        Length(max=500, message='الملاحظات طويلة جداً')
    ])


class CreateUserForm(FlaskForm):
    """Secure user creation form"""
    username = StringField('اسم المستخدم', validators=[
        DataRequired(message='اسم المستخدم مطلوب'),
        Length(min=3, max=80, message='اسم المستخدم يجب أن يكون بين 3 و 80 حرف'),
        Regexp(r'^[a-zA-Z0-9_]+$', message='اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة'),
        Length(min=8, message='كلمة المرور يجب أن تحتوي على 8 أحرف على الأقل')
    ])
    is_super_admin = BooleanField('مدير عام')


class PaymentForm(FlaskForm):
    """Secure payment processing form"""
    shipment_id = StringField('معرف الشحنة', validators=[
        DataRequired(message='معرف الشحنة مطلوب')
    ], widget=HiddenInput())
    
    payment_amount = DecimalField('مبلغ الدفع', validators=[
        DataRequired(message='مبلغ الدفع مطلوب'),
        NumberRange(min=0.001, message='مبلغ الدفع يجب أن يكون أكبر من الصفر')
    ], places=3)


class ExpenseForm(FlaskForm):
    """Secure expense form"""
    name = StringField('اسم المصروف', validators=[
        DataRequired(message='اسم المصروف مطلوب'),
        Length(min=2, max=200, message='اسم المصروف يجب أن يكون بين 2 و 200 حرف')
    ])
    amount = DecimalField('المبلغ', validators=[
        DataRequired(message='المبلغ مطلوب'),
        NumberRange(min=0.001, message='المبلغ يجب أن يكون أكبر من الصفر')
    ], places=3)
    category = StringField('الفئة', validators=[
        Optional(),
        Length(max=100, message='اسم الفئة طويل جداً')
    ])
    description = TextAreaField('الوصف', validators=[
        Optional(),
        Length(max=500, message='الوصف طويل جداً')
    ])


class RevenueForm(FlaskForm):
    """Secure revenue form"""
    name = StringField('اسم الإيراد', validators=[
        DataRequired(message='اسم الإيراد مطلوب'),
        Length(min=2, max=200, message='اسم الإيراد يجب أن يكون بين 2 و 200 حرف')
    ])
    amount = DecimalField('المبلغ', validators=[
        DataRequired(message='المبلغ مطلوب'),
        NumberRange(min=0.001, message='المبلغ يجب أن يكون أكبر من الصفر')
    ], places=3)
    revenue_type = SelectField('نوع الإيراد', choices=[
        ('general_shipments', 'إيرادات شحنات عامة'),
        ('documents', 'إيرادات مستندات'),
        ('other', 'إيرادات أخرى')
    ], validators=[DataRequired(message='نوع الإيراد مطلوب')])


def sanitize_input(input_string):
    """Sanitize user input to prevent XSS attacks"""
    if not input_string:
        return input_string
    
    # Remove potentially dangerous characters
    cleaned = re.sub(r'[<>"\']', '', str(input_string))
    
    # Remove script tags
    cleaned = re.sub(r'<script.*?</script>', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove javascript: protocols
    cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()


def validate_file_upload(file):
    """Validate uploaded files for security"""
    if not file:
        return False, "لم يتم اختيار ملف"
    
    # Check file size (max 10MB)
    if len(file.read()) > 10 * 1024 * 1024:
        return False, "حجم الملف كبير جداً (الحد الأقصى 10 ميجابايت)"
    
    file.seek(0)  # Reset file pointer
    
    # Check file extension
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.txt'}
    filename = file.filename.lower()
    
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return False, "نوع الملف غير مدعوم"
    
    # Check file signature/magic bytes for common file types
    file_header = file.read(10)
    file.seek(0)  # Reset file pointer
    
    safe_signatures = [
        b'\x89PNG',  # PNG
        b'\xff\xd8\xff',  # JPEG
        b'%PDF',  # PDF
        b'PK\x03\x04',  # ZIP/DOCX
        b'\xd0\xcf\x11\xe0',  # DOC
    ]
    
    if not any(file_header.startswith(sig) for sig in safe_signatures):
        return False, "نوع الملف غير آمن"
    
    return True, "الملف آمن"

class ChangePasswordForm(FlaskForm):
    """Simple password change form"""
    current_password = PasswordField('كلمة المرور الحالية', validators=[
        DataRequired(message='كلمة المرور الحالية مطلوبة')
    ])
    new_password = PasswordField('كلمة المرور الجديدة', validators=[
        DataRequired(message='كلمة المرور الجديدة مطلوبة'),
        Length(min=4, message='كلمة المرور يجب أن تحتوي على 4 أحرف على الأقل')
    ])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[
        DataRequired(message='تأكيد كلمة المرور مطلوب'),
        EqualTo('new_password', message='كلمات المرور غير متطابقة')
    ])
    submit = SubmitField('تغيير كلمة المرور')