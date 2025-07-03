# دليل تثبيت نظام إدارة الشحن على cPanel

## 📋 المتطلبات الأساسية
- استضافة cPanel مع دعم Python 3.11+
- قاعدة بيانات MySQL
- إمكانية رفع الملفات

## 🗄️ إعداد قاعدة البيانات MySQL

### 1. إنشاء قاعدة البيانات
```sql
-- في cPanel MySQL Databases
اسم قاعدة البيانات: shipping_system
اسم المستخدم: shipping_user
كلمة المرور: [اختر كلمة مرور قوية]
```

### 2. تشغيل سكريبت قاعدة البيانات
- ارفع ملف `database_schema.sql` إلى phpMyAdmin
- قم بتنفيذ السكريبت لإنشاء الجداول والبيانات الأساسية

## 📁 رفع الملفات

### الملفات المطلوبة:
```
public_html/shipping/
├── app.py
├── main.py
├── models.py
├── routes.py
├── translations.py
├── passenger_wsgi.py
├── .htaccess
├── requirements_cpanel.txt
├── setup_mysql.py
├── templates/
│   └── [جميع ملفات HTML]
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── instance/
    └── [مجلد فارغ]
```

## ⚙️ تكوين النظام

### 1. تحديث ملف .htaccess
```apache
# استبدل القيم التالية بمعلوماتك
SetEnv DATABASE_URL "mysql+pymysql://shipping_user:your_password@localhost/shipping_system"
SetEnv SESSION_SECRET "your-secure-random-session-key"
PassengerPython /home/cpanel_username/virtualenv/public_html/shipping/3.11/bin/python
PassengerAppRoot /home/cpanel_username/public_html/shipping
```

### 2. تثبيت المكتبات
```bash
pip install -r requirements_cpanel.txt
```

### 3. تشغيل الإعداد الأولي
```bash
python3 setup_mysql.py
```

## 🧪 اختبار التثبيت

### 1. زيارة الموقع
```
https://yourdomain.com/shipping/
```

### 2. تسجيل الدخول
```
اسم المستخدم: admin
كلمة المرور: admin123
```

### 3. اختبار الوظائف
- ✅ إنشاء شحنة جديدة
- ✅ طباعة الفواتير
- ✅ تتبع الشحنات
- ✅ إدارة الأنواع والأسعار

## 🔧 حل المشاكل الشائعة

### خطأ قاعدة البيانات
```
- تحقق من معلومات الاتصال في .htaccess
- تأكد من أن المستخدم له صلاحيات كاملة
- تحقق من أن قاعدة البيانات تدعم utf8mb4
```

### خطأ 500
```
- تحقق من مسار Python في PassengerPython
- تأكد من رفع جميع الملفات
- راجع error_log في cPanel
```

### CSS/JS لا يعمل
```
- تحقق من مسار مجلد static
- تأكد من أذونات الملفات (644)
- فعل mod_rewrite في .htaccess
```

## 🚀 التشغيل النهائي

بعد اكتمال جميع الخطوات:

1. **غيّر كلمة مرور الإدارة الافتراضية**
2. **أنشئ نسخة احتياطية من قاعدة البيانات**
3. **اختبر جميع الوظائف الأساسية**
4. **كوّن إعدادات الأسعار والمناطق**

---

## 📞 الدعم التقني

في حالة واجهت أي مشاكل:
- راجع ملفات السجلات في cPanel
- تحقق من إعدادات PHP وقاعدة البيانات
- تأكد من صحة مسارات الملفات

**النظام جاهز للاستخدام! 🎉**