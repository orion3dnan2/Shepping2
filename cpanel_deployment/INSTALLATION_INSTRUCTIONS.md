
# تعليمات التثبيت على cPanel

## 1. رفع الملفات
- ارفع جميع الملفات إلى مجلد public_html/shipping/
- تأكد من أن الأذونات صحيحة (644 للملفات، 755 للمجلدات)

## 2. إعداد قاعدة البيانات
- أنشئ قاعدة بيانات MySQL جديدة
- استورد ملف database_schema.sql
- حدث معلومات الاتصال في .htaccess

## 3. تكوين البيئة
- حدت مسار Python في .htaccess
- قم بتثبيت المكتبات: pip install -r requirements_cpanel.txt
- شغل: python3 setup_mysql.py

## 4. اختبار النظام
- زر: https://yourdomain.com/shipping/
- سجل دخول: admin / admin123
