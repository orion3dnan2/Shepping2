"""
Translation dictionaries for Arabic and English
"""

TRANSLATIONS = {
    'ar': {
        # Navigation
        'company_name': 'مرسال إكسبرس للاستيراد والتصدير',
        'dashboard': 'الصفحة الرئيسية',
        'shipments': 'الشحنات',
        'expenses': 'المصاريف',
        'reports': 'التقارير',
        'track_shipment': 'تتبع الشحنة',
        'logout': 'تسجيل الخروج',
        'login': 'تسجيل الدخول',
        
        # Dashboard
        'welcome': 'مرحباً بك في نظام إدارة الشحنات',
        'total_shipments': 'إجمالي الشحنات',
        'delivered': 'تم التوصيل',
        'in_transit': 'في الطريق',
        'pending': 'في الانتظار',
        'total_revenue': 'إجمالي الإيرادات',
        'quick_actions': 'إجراءات سريعة',
        'add_new_shipment': 'إضافة شحنة جديدة',
        'track_package': 'تتبع طرد',
        'view_reports': 'عرض التقارير',
        'manage_expenses': 'إدارة المصاريف',
        
        # Shipments
        'tracking_number': 'رقم التتبع',
        'sender_name': 'اسم المرسل',
        'receiver_name': 'اسم المستلم',
        'weight': 'الوزن',
        'status': 'الحالة',
        'created_date': 'تاريخ الإنشاء',
        'actions': 'الإجراءات',
        'view': 'عرض',
        'edit': 'تعديل',
        'delete': 'حذف',
        
        # Shipment Form
        'sender_info': 'بيانات المرسل',
        'receiver_info': 'بيانات المستلم',
        'shipment_details': 'تفاصيل الشحنة',
        'name': 'الاسم',
        'phone': 'الهاتف',
        'address': 'العنوان',
        'email': 'البريد الإلكتروني',
        'address_kuwait': 'العنوان في الكويت',
        'document_type': 'نوع المستند',
        'address_sudan': 'العنوان في السودان',
        'package_type': 'نوع الطرد',
        'package_contents': 'محتويات الطرد',
        'notes': 'ملاحظات',
        'direction': 'الاتجاه',
        'kuwait_to_sudan': 'من الكويت إلى السودان',
        'sudan_to_kuwait': 'من السودان إلى الكويت',
        'cost': 'التكلفة',
        'save': 'حفظ',
        'cancel': 'إلغاء',
        
        # Status
        'created': 'تم الإنشاء',
        'packaged': 'تم التغليف',
        'dispatching': 'جاري الإرسال',
        'shipped': 'تم الإرسال',
        'in_transit': 'في الطريق',
        'received': 'تم الاستلام',
        'delivered': 'تم التسليم',
        'cancelled': 'ملغي',
        
        # Tracking
        'shipment_tracking': 'تتبع الشحنة',
        'enter_tracking_number': 'أدخل رقم التتبع',
        'track': 'تتبع',
        'shipment_found': 'تم العثور على الشحنة',
        'shipment_not_found': 'لم يتم العثور على الشحنة',
        'current_status': 'الحالة الحالية',
        'creation_date': 'تاريخ الإنشاء',
        'contents': 'المحتويات',
        'personal_items': 'أغراض شخصية',
        
        # Common
        'search': 'بحث',
        'add': 'إضافة',
        'update': 'تحديث',
        'close': 'إغلاق',
        'back': 'رجوع',
        'next': 'التالي',
        'previous': 'السابق',
        'language': 'اللغة',
        'kg': 'كج',
        'kwd': 'د.ك',
        'required': 'مطلوب',
        'optional': 'اختياري',
        'settings': 'الإعدادات',
        'user_management': 'إدارة المستخدمين',
    },
    
    'en': {
        # Navigation
        'company_name': 'Morsal Express for Import and Export',
        'dashboard': 'Dashboard',
        'shipments': 'Shipments',
        'expenses': 'Expenses',
        'reports': 'Reports',
        'track_shipment': 'Track Shipment',
        'logout': 'Logout',
        'login': 'Login',
        
        # Dashboard
        'welcome': 'Welcome to Shipment Management System',
        'total_shipments': 'Total Shipments',
        'delivered': 'Delivered',
        'in_transit': 'In Transit',
        'pending': 'Pending',
        'total_revenue': 'Total Revenue',
        'quick_actions': 'Quick Actions',
        'add_new_shipment': 'Add New Shipment',
        'track_package': 'Track Package',
        'view_reports': 'View Reports',
        'manage_expenses': 'Manage Expenses',
        
        # Shipments
        'tracking_number': 'Tracking Number',
        'sender_name': 'Sender Name',
        'receiver_name': 'Receiver Name',
        'weight': 'Weight',
        'status': 'Status',
        'created_date': 'Created Date',
        'actions': 'Actions',
        'view': 'View',
        'edit': 'Edit',
        'delete': 'Delete',
        
        # Shipment Form
        'sender_info': 'Sender Information',
        'receiver_info': 'Receiver Information',
        'shipment_details': 'Shipment Details',
        'name': 'Name',
        'phone': 'Phone',
        'address': 'Address',
        'email': 'Email',
        'address_kuwait': 'Address in Kuwait',
        'document_type': 'Document Type',
        'address_sudan': 'Address in Sudan',
        'package_type': 'Package Type',
        'package_contents': 'Package Contents',
        'notes': 'Notes',
        'direction': 'Direction',
        'kuwait_to_sudan': 'Kuwait to Sudan',
        'sudan_to_kuwait': 'Sudan to Kuwait',
        'cost': 'Cost',
        'save': 'Save',
        'cancel': 'Cancel',
        
        # Status
        'created': 'Created',
        'packaged': 'Packaged',
        'dispatching': 'Dispatching',
        'shipped': 'Shipped',
        'in_transit': 'In Transit',
        'received': 'Received',
        'delivered': 'Delivered',
        'cancelled': 'Cancelled',
        
        # Tracking
        'shipment_tracking': 'Shipment Tracking',
        'enter_tracking_number': 'Enter Tracking Number',
        'track': 'Track',
        'shipment_found': 'Shipment Found',
        'shipment_not_found': 'Shipment Not Found',
        'current_status': 'Current Status',
        'creation_date': 'Creation Date',
        'contents': 'Contents',
        'personal_items': 'Personal Items',
        
        # Common
        'search': 'Search',
        'add': 'Add',
        'update': 'Update',
        'close': 'Close',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'language': 'Language',
        'kg': 'kg',
        'kwd': 'KWD',
        'required': 'Required',
        'optional': 'Optional',
        'settings': 'Settings',
        'user_management': 'User Management',
    }
}

def get_text(key, language='ar'):
    """Get translated text for a given key and language"""
    return TRANSLATIONS.get(language, {}).get(key, key)