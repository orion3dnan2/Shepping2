# دليل حل خطأ 503 - نظام إدارة الشحن

## 🚨 المشاكل المكتشفة في التكوين الحالي:

### 1. ترتيب متغيرات البيئة في .htaccess
**المشكلة:** متغيرات البيئة يجب أن تكون في بداية الملف
**الحل:** استخدم `.htaccess_fixed` المرفق

### 2. إعدادات Passenger ناقصة
**المشكلة:** عدم وجود إعدادات متقدمة لـ Passenger
**الحل:** إضافة:
```apache
PassengerFriendlyErrorPages On
PassengerMinInstances 1
PassengerMaxPoolSize 6
```

### 3. معالجة أخطاء WSGI محدودة
**المشكلة:** passenger_wsgi.py لا يوفر تشخيص كافي
**الحل:** استخدم `passenger_wsgi_fixed.py`

## ✅ الحلول المقترحة:

### الحل الأول: استبدال الملفات المحسنة
```bash
# استبدل الملفات التالية:
cp .htaccess_fixed .htaccess
cp passenger_wsgi_fixed.py passenger_wsgi.py
```

### الحل الثاني: فحص المتطلبات الأساسية
```bash
# 1. تحقق من مسار Python:
which python3
# النتيجة يجب أن تكون شيء مثل:
# /home/username/virtualenv/public_html/shipping/3.11/bin/python

# 2. تحقق من المكتبات:
pip list | grep Flask
pip list | grep SQLAlchemy

# 3. اختبر الاستيراد:
python3 -c "from app import app; print('OK')"
```

### الحل الثالث: إعدادات cPanel المطلوبة
```
1. في cPanel → Python Apps:
   - تأكد من تفعيل Python 3.11+
   - تحديد مجلد التطبيق الصحيح

2. في MySQL Databases:
   - تأكد من صحة اسم قاعدة البيانات
   - تأكد من صلاحيات المستخدم الكاملة

3. في File Manager:
   - تحقق من أذونات الملفات
   - تأكد من وجود جميع الملفات
```

## 🔧 خطوات التشخيص المفصلة:

### 1. فحص سجلات الأخطاء
```
cPanel → Error Logs → اقرأ آخر 50 سطر
ابحث عن:
- ModuleNotFoundError
- Permission denied
- Database connection error
```

### 2. اختبار التكوين خطوة بخطوة
```bash
# الخطوة 1: اختبر Python
python3 --version

# الخطوة 2: اختبر Flask
python3 -c "import flask; print(flask.__version__)"

# الخطوة 3: اختبر قاعدة البيانات
python3 -c "import pymysql; print('PyMySQL works')"

# الخطوة 4: اختبر التطبيق
python3 -c "from app import app; print('App imported successfully')"
```

### 3. فحص ملف التكوين
```apache
# تأكد من أن .htaccess يحتوي على:
SetEnv DATABASE_URL "mysql+pymysql://user:pass@localhost/db"
PassengerPython /path/to/python
PassengerEnabled On
```

## 🚀 الحل السريع (خطوات مرتبة):

### المرحلة 1: إعداد الملفات
1. انسخ `.htaccess_fixed` إلى `.htaccess`
2. انسخ `passenger_wsgi_fixed.py` إلى `passenger_wsgi.py`
3. حدث مسار Python في `.htaccess`

### المرحلة 2: تحديث قاعدة البيانات
1. تأكد من إنشاء قاعدة البيانات
2. استورد `database_schema.sql`
3. حدث معلومات الاتصال في `.htaccess`

### المرحلة 3: تثبيت المكتبات
```bash
cd public_html/shipping
pip install -r requirements_cpanel.txt
```

### المرحلة 4: اختبار النظام
1. زر الموقع
2. إذا ظهر خطأ، فحص Error Logs
3. استخدم معلومات التشخيص المحسنة

## 📋 قائمة تحقق نهائية:

- [ ] Python 3.11+ مثبت ومتاح
- [ ] جميع الملفات مرفوعة بأذونات صحيحة
- [ ] قاعدة بيانات MySQL منشأة ومستوردة
- [ ] معلومات الاتصال في .htaccess صحيحة
- [ ] مسار Python في .htaccess صحيح
- [ ] المكتبات مثبتة: Flask, SQLAlchemy, PyMySQL
- [ ] Passenger مفعل في cPanel
- [ ] لا توجد أخطاء في Error Logs

## 💡 نصائح إضافية:

1. **جرب استضافة مختلفة** إذا استمرت المشاكل
2. **اتصل بدعم الاستضافة** للحصول على مسار Python الصحيح
3. **ابدأ بتطبيق بسيط** لاختبار Passenger أولاً
4. **استخدم الملفات المحسنة** المرفقة في هذا الدليل

بهذه الحلول يجب أن يختفي خطأ 503 ويعمل النظام بشكل طبيعي!