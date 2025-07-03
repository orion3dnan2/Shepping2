# قائمة ملفات النشر على cPanel - مراجعة نهائية

## ✅ الملفات الأساسية المطلوبة

### ملفات التطبيق الأساسية
- [x] `app.py` - إعدادات Flask مع تحسينات cPanel
- [x] `main.py` - نقطة البداية مع دعم cPanel
- [x] `models.py` - نماذج قاعدة البيانات MySQL
- [x] `routes.py` - معالجات المسارات
- [x] `translations.py` - دعم اللغة العربية

### ملفات التكوين لـ cPanel
- [x] `passenger_wsgi.py` - WSGI entry point
- [x] `.htaccess` - إعدادات Apache و متغيرات البيئة
- [x] `requirements_cpanel.txt` - مكتبات Python للاستضافة

### ملفات المساعدة والإعداد
- [x] `app_start.py` - مساعد إعداد قاعدة البيانات
- [x] `cpanel_config.py` - مساعد التكوين والتحقق
- [x] `CPANEL_DEPLOYMENT.md` - دليل التثبيت التفصيلي
- [x] `README_CPANEL.md` - دليل شامل للمستخدم

### المجلدات المطلوبة
- [x] `templates/` - قوالب HTML (934 ملف)
- [x] `static/` - ملفات CSS، JS، الصور (76 ملف)
- [x] `migrations/` - ملفات ترحيل قاعدة البيانات

## 🔧 التحديثات المُطبقة لـ cPanel

### 1. إعدادات قاعدة البيانات
```python
# في app.py - تحسينات خاصة بـ cPanel
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 3,  # حجم مجموعة صغير للاستضافة المشتركة
    "max_overflow": 2,  # حد أقصى للاتصالات الإضافية
    "pool_recycle": 3600,  # إعادة تدوير الاتصالات كل ساعة
    "connect_args": {
        "charset": "utf8mb4"  # دعم النصوص العربية
    }
}
```

### 2. إعدادات Passenger
```python
# passenger_wsgi.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from main import app as application
```

### 3. إعدادات Apache
```apache
# .htaccess
PassengerEnabled on
PassengerPython /home/username/virtualenv/public_html/3.11/bin/python
SetEnv DATABASE_URL "mysql+pymysql://user:pass@localhost/db"
```

## 🚀 خطوات النشر السريع

### 1. رفع الملفات
```bash
# رفع هذه الملفات إلى public_html
app.py
main.py
models.py
routes.py
translations.py
passenger_wsgi.py
.htaccess
requirements_cpanel.txt
app_start.py
templates/
static/
```

### 2. إعداد قاعدة البيانات
```sql
CREATE DATABASE username_shipping CHARACTER SET utf8mb4;
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_pass';
GRANT ALL PRIVILEGES ON username_shipping.* TO 'app_user'@'localhost';
```

### 3. تحديث .htaccess
```apache
SetEnv DATABASE_URL "mysql+pymysql://app_user:secure_pass@localhost/username_shipping"
SetEnv SESSION_SECRET "random-secure-key-here"
PassengerPython /home/username/virtualenv/public_html/3.11/bin/python
```

### 4. تثبيت المكتبات
```bash
cd public_html
python3 -m pip install -r requirements_cpanel.txt
```

### 5. تشغيل الإعداد الأولي
```bash
python3 app_start.py
```

## ⚠️ نقاط مهمة

### الأمان
- تغيير SESSION_SECRET إلى مفتاح آمن
- تحديث كلمة مرور قاعدة البيانات
- تحديث كلمة مرور المشرف الافتراضية

### الأداء
- حجم مجموعة الاتصالات محدود (3-5 اتصالات)
- إعدادات التخزين المؤقت مُفعلة
- ضغط الملفات مُفعل

### الدعم الفني
- جميع الملفات متوافقة مع Python 3.11+
- قاعدة البيانات تدعم UTF8MB4 للنصوص العربية
- التطبيق مُحسن للاستضافة المشتركة

## 📊 الحالة النهائية
✅ **جاهز للنشر على cPanel**
- جميع الملفات موجودة ومُحدثة
- التكوين محسن للاستضافة المشتركة
- الوثائق شاملة ومفصلة
- أدوات المساعدة والتشخيص متوفرة

---
**آخر تحديث**: 3 يوليو 2025