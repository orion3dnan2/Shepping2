# دليل نشر التطبيق على cPanel

## المتطلبات الأساسية
- cPanel hosting account with Python support
- MySQL database access
- SSH access (optional but recommended)

## خطوات التثبيت

### 1. رفع الملفات
قم برفع جميع ملفات المشروع إلى مجلد `public_html` في cPanel:
```
/home/username/public_html/
├── app.py
├── main.py
├── passenger_wsgi.py
├── models.py
├── routes.py
├── translations.py
├── requirements_cpanel.txt
├── .htaccess
├── templates/
├── static/
└── migrations/
```

### 2. إعداد قاعدة البيانات MySQL
1. من cPanel، اذهب إلى "MySQL Databases"
2. أنشئ قاعدة بيانات جديدة (مثال: `username_shipping`)
3. أنشئ مستخدم MySQL جديد
4. أضف المستخدم إلى قاعدة البيانات مع جميع الصلاحيات

### 3. إعداد متغيرات البيئة
قم بتحديث ملف `.htaccess` بالمعلومات الصحيحة:
```apache
SetEnv DATABASE_URL "mysql+pymysql://username:password@localhost/database_name"
SetEnv SESSION_SECRET "your-secure-secret-key-here"
```

### 4. تثبيت Python Virtual Environment
```bash
# من SSH أو Terminal في cPanel
cd public_html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_cpanel.txt
```

### 5. تحديث مسار Python في .htaccess
```apache
PassengerPython /home/username/public_html/venv/bin/python
```

### 6. إعداد قاعدة البيانات
```bash
# تشغيل Migration لإنشاء الجداول
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## إعدادات MySQL المطلوبة

### في cPanel MySQL
- Character Set: `utf8mb4`
- Collation: `utf8mb4_unicode_ci`
- Engine: `InnoDB`

### في قاعدة البيانات
```sql
-- تأكد من إعدادات UTF8MB4
ALTER DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## تكوين البيئة الإنتاجية

### متغيرات البيئة المطلوبة
```
DATABASE_URL=mysql+pymysql://username:password@localhost/database_name
SESSION_SECRET=your-very-secure-secret-key
FLASK_ENV=production
```

### إعدادات الأمان
1. تغيير `SESSION_SECRET` إلى مفتاح آمن
2. تأكد من أن قاعدة البيانات محمية بكلمة مرور قوية
3. تحديث صلاحيات الملفات:
   ```bash
   chmod 644 *.py
   chmod 755 passenger_wsgi.py
   chmod 644 .htaccess
   ```

## استكشاف الأخطاء

### إذا لم يعمل التطبيق
1. تحقق من ملف Error Log في cPanel
2. تأكد من صحة معلومات قاعدة البيانات
3. تأكد من تثبيت جميع المكتبات المطلوبة
4. تحقق من مسار Python في `.htaccess`

### أخطاء قاعدة البيانات الشائعة
```
Error: Access denied for user
- تحقق من اسم المستخدم وكلمة المرور

Error: Unknown database
- تأكد من إنشاء قاعدة البيانات

Error: Connection refused
- تأكد من أن MySQL يعمل على الخادم
```

## إنشاء حساب الإدارة الأول
بعد التثبيت، قم بإنشاء حساب إدارة:
```bash
python3 -c "
from app import app, db
from models import Admin
with app.app_context():
    admin = Admin(username='admin', is_super_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created successfully')
"
```

## الدعم الفني
- تأكد من أن موفر الاستضافة يدعم Python 3.11+
- تحقق من دعم MySQL مع PyMySQL
- تأكد من تمكين Passenger للـ Python applications