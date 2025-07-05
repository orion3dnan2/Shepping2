# نشر النظام على منصة Render

## الميزات الأمنية المطبقة:

✅ **أمان قاعدة البيانات**
- استخدام PostgreSQL مع اتصال آمن SSL
- متغيرات البيئة للاتصال بقاعدة البيانات
- حماية من SQL Injection عبر SQLAlchemy ORM

✅ **أمان الجلسات**
- مفتاح جلسة آمن (SESSION_SECRET)
- حماية CSRF من خلال Flask-Login
- تشفير كلمات المرور باستخدام Werkzeug

✅ **أمان الخادم**
- ProxyFix للعمل خلف Load Balancer
- حد أقصى لحجم الملفات (16MB)
- تسجيل الأخطاء والأنشطة

## خطوات النشر على Render:

### 1. إنشاء حساب Render
- اذهب إلى https://render.com
- أنشئ حساب جديد أو سجل دخول

### 2. اتصال GitHub
- اربط حسابك بـ GitHub
- ارفع الكود إلى GitHub repository

### 3. إنشاء Web Service
- اختر "New Web Service"
- حدد GitHub repository الخاص بك
- اختر الإعدادات التالية:
  - **Build Command**: `pip install -r pyproject.toml`
  - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
  - **Python Version**: Python 3.11

### 4. إعداد متغيرات البيئة
أضف المتغيرات التالية في Render:

```
DATABASE_URL=postgresql://user:password@host:port/database
SESSION_SECRET=your-super-secret-key-here
```

### 5. إنشاء قاعدة البيانات
- أنشئ PostgreSQL database في Render
- انسخ DATABASE_URL من لوحة التحكم

### 6. النشر
- انقر على "Deploy"
- انتظر حتى يكتمل النشر
- الموقع سيكون متاحاً على: https://your-app.onrender.com

## الملفات المطلوبة للنشر:

1. ✅ `app.py` - التطبيق الرئيسي
2. ✅ `main.py` - نقطة الدخول
3. ✅ `models.py` - نماذج قاعدة البيانات
4. ✅ `routes.py` - المسارات والوظائف
5. ✅ `translations.py` - الترجمات
6. ✅ `pyproject.toml` - المتطلبات
7. ✅ `static/` - الملفات الثابتة
8. ✅ `templates/` - القوالب

## بيانات الدخول الافتراضية:
- **اسم المستخدم**: admin
- **كلمة المرور**: admin123

## الأمان في الإنتاج:
⚠️ **تذكر تغيير كلمة المرور الافتراضية** بعد النشر!

النظام جاهز 100% للنشر الآمن على Render.