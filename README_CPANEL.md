# نظام إدارة الشحن - دليل النشر على cPanel

## نظرة عامة
نظام إدارة الشحن المتطور باللغة العربية المصمم للعمل على خوادم cPanel. النظام يدعم إدارة الشحنات، المستندات، والتقارير المالية بشكل متكامل.

## المتطلبات التقنية
- **Python**: 3.11 أو أحدث
- **قاعدة البيانات**: MySQL 5.7+ أو MariaDB 10.3+
- **استضافة**: cPanel مع دعم Python و Passenger
- **ذاكرة**: 512 MB RAM كحد أدنى
- **مساحة**: 100 MB للتطبيق + مساحة قاعدة البيانات

## ملفات النشر المطلوبة

### الملفات الأساسية
- `passenger_wsgi.py` - نقطة دخول WSGI لـ cPanel
- `.htaccess` - إعدادات Apache و متغيرات البيئة
- `requirements_cpanel.txt` - مكتبات Python المطلوبة
- `app_start.py` - مساعد إعداد قاعدة البيانات
- `cpanel_config.py` - مساعد التكوين

### ملفات التطبيق
- `app.py` - إعدادات Flask الأساسية
- `main.py` - نقطة بداية التطبيق
- `models.py` - نماذج قاعدة البيانات
- `routes.py` - معالجات URL
- `translations.py` - دعم اللغة العربية

### المجلدات المطلوبة
- `templates/` - قوالب HTML
- `static/` - ملفات CSS، JS، والصور
- `migrations/` - ملفات ترحيل قاعدة البيانات

## خطوات التثبيت السريع

### 1. إعداد قاعدة البيانات
```sql
-- إنشاء قاعدة البيانات
CREATE DATABASE username_shipping CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- إنشاء مستخدم قاعدة البيانات
CREATE USER 'username_app'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON username_shipping.* TO 'username_app'@'localhost';
FLUSH PRIVILEGES;
```

### 2. تحديث .htaccess
```apache
# استبدل القيم بالمعلومات الحقيقية
SetEnv DATABASE_URL "mysql+pymysql://username_app:secure_password@localhost/username_shipping"
SetEnv SESSION_SECRET "your-very-secure-random-secret-key"
PassengerPython /home/username/virtualenv/public_html/3.11/bin/python
```

### 3. تثبيت المكتبات
```bash
cd public_html
python3 -m pip install -r requirements_cpanel.txt
```

### 4. تشغيل الإعداد الأولي
```bash
python3 app_start.py
```

## التكوين المتقدم

### إعدادات الأمان
```apache
# في .htaccess
# فرض HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# حماية الملفات الحساسة
<Files "*.py">
    Order allow,deny
    Deny from all
</Files>
```

### إعدادات الأداء
```apache
# ضغط الملفات
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript
</IfModule>

# التخزين المؤقت
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 year"
</IfModule>
```

## استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### خطأ: "Application failed to start"
```bash
# تحقق من ملف الأخطاء
tail -f ~/logs/username.com/error.log

# تحقق من مسار Python
which python3
```

#### خطأ: "Database connection failed"
```bash
# اختبار الاتصال بقاعدة البيانات
python3 -c "import pymysql; print('PyMySQL imported successfully')"
```

#### خطأ: "Permission denied"
```bash
# إعداد صلاحيات الملفات
chmod 755 passenger_wsgi.py
chmod 644 *.py
chmod 644 .htaccess
```

### تشخيص المشاكل
```bash
# تشغيل أدوات التشخيص
python3 cpanel_config.py

# تحقق من المكتبات المثبتة
python3 -c "import flask, pymysql, sqlalchemy; print('All packages OK')"
```

## إدارة التطبيق

### إنشاء المستخدمين
```bash
# إنشاء مستخدم إدارة جديد
python3 -c "
from app import app, db
from models import Admin
with app.app_context():
    admin = Admin(username='new_admin', is_super_admin=False)
    admin.set_password('secure_password')
    admin.set_permissions({'home': True, 'shipments': True})
    db.session.add(admin)
    db.session.commit()
"
```

### النسخ الاحتياطي
```bash
# نسخ احتياطي لقاعدة البيانات
mysqldump -u username_app -p username_shipping > backup_$(date +%Y%m%d).sql

# نسخ احتياطي للملفات
tar -czf app_backup_$(date +%Y%m%d).tar.gz *.py templates/ static/
```

## الترقية والصيانة

### ترقية التطبيق
```bash
# تحديث المكتبات
python3 -m pip install --upgrade -r requirements_cpanel.txt

# تشغيل الترحيل
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### مراقبة الأداء
```bash
# تحقق من استخدام الذاكرة
ps aux | grep python

# تحقق من حالة قاعدة البيانات
mysql -u username_app -p -e "SHOW PROCESSLIST;"
```

## الدعم الفني

### معلومات الاتصال
- البريد الإلكتروني: support@yourcompany.com
- الهاتف: +1-XXX-XXX-XXXX

### الوثائق الإضافية
- [دليل المستخدم](USER_GUIDE.md)
- [دليل المطور](DEVELOPER_GUIDE.md)
- [الأسئلة الشائعة](FAQ.md)

## الترخيص
هذا النظام مرخص تحت [MIT License](LICENSE)

---
**تم تطوير هذا النظام بواسطة فريق التطوير المتخصص في أنظمة إدارة الشحن**