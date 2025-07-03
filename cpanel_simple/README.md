# نظام إدارة الشحن - حزمة النشر المبسطة

## الملفات الأساسية (جاهزة للنشر)

### ملفات Python:
- `app.py` - تطبيق Flask الرئيسي
- `main.py` - نقطة الدخول
- `models.py` - نماذج قاعدة البيانات (15 جدول)
- `routes.py` - مسارات التطبيق
- `translations.py` - دعم اللغتين العربية والإنجليزية

### ملفات التكوين:
- `passenger_wsgi.py` - محرك WSGI لـ cPanel
- `.htaccess` - إعدادات Apache
- `requirements_cpanel.txt` - المكتبات المطلوبة
- `database_schema.sql` - مخطط قاعدة البيانات MySQL

### واجهة المستخدم:
- `templates/` - صفحات HTML (24 ملف)
- `static/` - ملفات CSS وJS والصور
- `instance/` - مجلد البيانات

## خطوات النشر:

### 1. رفع الملفات
```bash
# ارفع جميع الملفات إلى:
public_html/shipping/
```

### 2. إعداد قاعدة البيانات
```sql
-- أنشئ قاعدة بيانات MySQL
-- استورد database_schema.sql
```

### 3. تحديث .htaccess
```apache
# حدث معلومات قاعدة البيانات:
SetEnv DATABASE_URL "mysql+pymysql://user:password@localhost/database"
```

### 4. تثبيت المكتبات
```bash
pip install -r requirements_cpanel.txt
```

### 5. تشغيل النظام
```
https://موقعك.com/shipping/
المستخدم: admin
كلمة المرور: admin123
```

## المميزات:
- ✅ دعم اللغتين العربية والإنجليزية
- ✅ إدارة الشحنات والتتبع
- ✅ نظام مالي شامل
- ✅ طباعة الفواتير
- ✅ تقارير مفصلة
- ✅ أمان متقدم

النظام جاهز للاستخدام الفوري!