from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms.widgets import TextArea, HiddenInput
import html

class SecureForm(FlaskForm):
    """Base form class with security features"""
    
    def validate_input(self, field):
        """Escape HTML and validate input"""
        if field.data:
            field.data = html.escape(field.data.strip())
        return True

class LoginForm(SecureForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(message='اسم المستخدم مطلوب')])
    password = PasswordField('كلمة المرور', validators=[DataRequired(message='كلمة المرور مطلوبة')])

class ShipmentForm(SecureForm):
    # Sender Information
    sender_name = StringField('اسم المرسل', validators=[Optional(), Length(max=100)])
    sender_phone = StringField('هاتف المرسل', validators=[Optional(), Length(max=50)])
    sender_address = TextAreaField('عنوان المرسل', validators=[Optional(), Length(max=200)])
    sender_email = StringField('بريد المرسل', validators=[Optional(), Email(message='البريد الإلكتروني غير صحيح'), Length(max=100)])
    
    # Receiver Information
    receiver_name = StringField('اسم المستلم', validators=[Optional(), Length(max=100)])
    receiver_phone = StringField('هاتف المستلم', validators=[Optional(), Length(max=50)])
    receiver_address = TextAreaField('عنوان المستلم', validators=[Optional(), Length(max=200)])
    receiver_email = StringField('بريد المستلم', validators=[Optional(), Email(message='البريد الإلكتروني غير صحيح'), Length(max=100)])
    
    # Shipment Details
    direction = SelectField('الاتجاه', choices=[
        ('kuwait_to_sudan', 'من الكويت إلى السودان'),
        ('sudan_to_kuwait', 'من السودان إلى الكويت')
    ], default='kuwait_to_sudan')
    
    package_type = SelectField('نوع الشحنة', choices=[
        ('general', 'شحنة عامة'),
        ('document', 'مستندات')
    ], default='general')
    
    shipping_method = SelectField('طريقة الشحن', choices=[
        ('جوي', 'جوي'),
        ('بري', 'بري')
    ], validators=[Optional()])
    
    weight = FloatField('الوزن (كيلو)', validators=[Optional(), NumberRange(min=0.001, max=1000, message='الوزن يجب أن يكون بين 0.001 و 1000 كيلو')])
    zone = SelectField('المنطقة', validators=[Optional()])
    packaging = SelectField('نوع التغليف', validators=[Optional()])
    
    # Document specific fields
    document_type = SelectField('نوع المستند', validators=[Optional()])
    action_required = StringField('الإجراء المطلوب', validators=[Optional(), Length(max=200)])
    
    # Pricing
    price = FloatField('السعر الإجمالي', validators=[Optional(), NumberRange(min=0, max=999999, message='السعر يجب أن يكون بين 0 و 999999')])
    cost = FloatField('التكلفة', validators=[Optional(), NumberRange(min=0, max=999999, message='التكلفة يجب أن تكون بين 0 و 999999')], widget=HiddenInput())
    paid_amount = FloatField('المبلغ المدفوع', validators=[Optional(), NumberRange(min=0, max=999999, message='المبلغ المدفوع يجب أن يكون بين 0 و 999999')])
    
    # Additional options
    has_packaging = BooleanField('تغليف')
    has_policy = BooleanField('سياسة/بوليصة')
    has_comment = BooleanField('تعليق')
    waybill_price = FloatField('سعر البوليصة', validators=[Optional(), NumberRange(min=0, max=999999, message='سعر البوليصة يجب أن يكون بين 0 و 999999')])
    
    # Content
    package_contents = TextAreaField('محتويات الشحنة', validators=[Optional(), Length(max=200)])
    notes = TextAreaField('ملاحظات', validators=[Optional(), Length(max=500)])

class FinancialTransactionForm(SecureForm):
    name = StringField('اسم المعاملة', validators=[DataRequired(message='اسم المعاملة مطلوب'), Length(max=200)])
    amount = FloatField('المبلغ', validators=[DataRequired(message='المبلغ مطلوب'), NumberRange(min=0.001, max=999999, message='المبلغ يجب أن يكون بين 0.001 و 999999')])
    category = StringField('الفئة', validators=[Optional(), Length(max=100)])
    shipping_type = SelectField('نوع الشحن', choices=[
        ('شحن بري', 'شحن بري'),
        ('شحن جوي', 'شحن جوي'),
        ('مستندات', 'مستندات')
    ], validators=[Optional()])
    revenue_type = SelectField('نوع الإيراد', choices=[
        ('general_shipments', 'إيرادات شحنات عامة'),
        ('documents', 'إيرادات مستندات'),
        ('other', 'إيرادات أخرى')
    ], validators=[Optional()])
    description = TextAreaField('الوصف', validators=[Optional(), Length(max=500)])

class UserForm(SecureForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(message='اسم المستخدم مطلوب'), Length(min=3, max=80, message='اسم المستخدم يجب أن يكون بين 3 و 80 حرف')])
    password = PasswordField('كلمة المرور', validators=[Optional(), Length(min=6, max=50, message='كلمة المرور يجب أن تكون بين 6 و 50 حرف')])
    is_super_admin = BooleanField('مدير عام')
    
    # Permissions
    home_permission = BooleanField('صفحة الرئيسية')
    shipments_permission = BooleanField('الشحنات')
    tracking_permission = BooleanField('تتبع الشحنات')
    reports_permission = BooleanField('التقارير')
    expenses_permission = BooleanField('المصروفات')
    add_shipment_permission = BooleanField('إضافة شحنة')
    settings_permission = BooleanField('الإعدادات')

class ShippingTypeForm(SecureForm):
    name_ar = StringField('الاسم بالعربية', validators=[DataRequired(message='الاسم بالعربية مطلوب'), Length(max=100)])
    name_en = StringField('الاسم بالإنجليزية', validators=[DataRequired(message='الاسم بالإنجليزية مطلوب'), Length(max=100)])
    price = FloatField('السعر', validators=[DataRequired(message='السعر مطلوب'), NumberRange(min=0, max=999999, message='السعر يجب أن يكون بين 0 و 999999')])

class DocumentTypeForm(SecureForm):
    name_ar = StringField('الاسم بالعربية', validators=[DataRequired(message='الاسم بالعربية مطلوب'), Length(max=100)])
    name_en = StringField('الاسم بالإنجليزية', validators=[DataRequired(message='الاسم بالإنجليزية مطلوب'), Length(max=100)])
    price = FloatField('السعر', validators=[DataRequired(message='السعر مطلوب'), NumberRange(min=0, max=999999, message='السعر يجب أن يكون بين 0 و 999999')])

class PaymentForm(SecureForm):
    amount = FloatField('المبلغ', validators=[DataRequired(message='المبلغ مطلوب'), NumberRange(min=0.001, max=999999, message='المبلغ يجب أن يكون بين 0.001 و 999999')])

class TrackingForm(SecureForm):
    tracking_number = StringField('رقم التتبع', validators=[DataRequired(message='رقم التتبع مطلوب'), Length(max=20)])

class AirShippingCostsForm(SecureForm):
    price_per_kg = FloatField('سعر الكيلو/طيران', validators=[DataRequired(message='سعر الكيلو مطلوب'), NumberRange(min=0, max=999999)])
    packaging_price = FloatField('سعر التغليف', validators=[DataRequired(message='سعر التغليف مطلوب'), NumberRange(min=0, max=999999)])
    kuwait_transport_price = FloatField('سعر الترحيل في الكويت', validators=[DataRequired(message='سعر الترحيل في الكويت مطلوب'), NumberRange(min=0, max=999999)])
    sudan_transport_price = FloatField('سعر الترحيل في السودان', validators=[DataRequired(message='سعر الترحيل في السودان مطلوب'), NumberRange(min=0, max=999999)])
    clearance_price = FloatField('سعر التخليص', validators=[DataRequired(message='سعر التخليص مطلوب'), NumberRange(min=0, max=999999)])

class DocumentCostsForm(SecureForm):
    doc_authentication_foreign = FloatField('توثيق خارجية', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_authentication_education = FloatField('توثيق تعليم عالي', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_criminal_record = FloatField('أدلة جنائية/فيش', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_secondary_certificate = FloatField('استخراج شهادة ثانوية', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_university_certificate = FloatField('استخراج شهادة جامعية', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_marriage_registered = FloatField('استخراج قسيمة زواج مدرجة', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_marriage_unregistered = FloatField('استخراج قسيمة زواج غير مدرجة', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    doc_university_details = FloatField('استخراج شهادة جامعية تفاصيل', validators=[DataRequired(), NumberRange(min=0, max=999999)])