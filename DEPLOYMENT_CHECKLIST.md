# قائمة فحص نشر نظام مرسال إكسبرس

## الملفات الأساسية المطلوبة ✓

### 1. ملفات التطبيق الأساسية:
- ✅ `app.py` - إعداد Flask وقاعدة البيانات
- ✅ `main.py` - نقطة دخول التطبيق
- ✅ `models.py` - نماذج قاعدة البيانات (15 جدول)
- ✅ `routes.py` - مسارات التطبيق
- ✅ `translations.py` - ملف الترجمة العربية/الإنجليزية

### 2. ملفات إدارة التبعيات:
- ✅ `pyproject.toml` - تبعيات Python (12 مكتبة)
- ✅ `uv.lock` - قفل التبعيات

### 3. ملفات النشر:
- ✅ `Procfile` - إعداد النشر للمنصات السحابية
- ✅ `.flaskenv` - متغيرات بيئة Flask
- ✅ `README.md` - تعليمات التثبيت والنشر

### 4. ملفات قاعدة البيانات:
- ✅ `migrations/` - مجلد ترحيل قاعدة البيانات
- ✅ `migrations/alembic.ini` - إعداد Alembic
- ✅ `migrations/env.py` - بيئة المهاجرة
- ✅ `migrations/versions/` - إصدارات المهاجرة

### 5. ملفات الواجهة:
- ✅ `templates/` - قوالب HTML (25 ملف)
- ✅ `static/` - ملفات CSS/JS

## التبعيات المطلوبة من pyproject.toml:

```toml
[project]
dependencies = [
    "flask>=3.1.1",
    "flask-sqlalchemy>=3.1.1", 
    "flask-migrate>=4.0.0",
    "flask-login>=0.6.3",
    "flask-dance>=7.1.0",
    "psycopg2-binary>=2.9.10",
    "gunicorn>=23.0.0",
    "email-validator>=2.2.0",
    "sqlalchemy>=2.0.41",
    "werkzeug>=3.1.3",
    "pyjwt>=2.10.1",
    "oauthlib>=3.3.1"
]
```

## متغيرات البيئة المطلوبة:

```env
DATABASE_URL=postgresql://username:password@host:port/database
SESSION_SECRET=your-secret-key-here
FLASK_ENV=production
```

## حالة قاعدة البيانات PostgreSQL:

✅ **الجداول المنشأة (15 جدول):**
1. admin - إدارة المستخدمين
2. air_shipping_costs - تكاليف الشحن الجوي
3. alembic_version - إصدارات المهاجرة
4. document_costs - تكاليف المستندات
5. document_type - أنواع المستندات
6. expenses_documents - مصروفات المستندات
7. expenses_general - المصروفات العامة
8. financial_transaction - المعاملات المالية
9. global_settings - الإعدادات العامة
10. notification - الإشعارات
11. operational_cost - التكاليف التشغيلية
12. packaging_type - أنواع التغليف
13. shipment - الشحنات (الجدول الرئيسي)
14. shipment_type - أنواع الشحنات
15. zone_pricing - أسعار المناطق

✅ **البيانات المهاجرة:**
- 19 شحنة محفوظة
- 2 مستخدم admin
- جميع الإعدادات والتكوينات

## أوامر التشغيل:

### محلياً (التطوير):
```bash
python main.py
```

### الإنتاج:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

## نشر على المنصات السحابية:

### Render/Heroku/Railway:
1. ربط المستودع
2. تعيين متغيرات البيئة
3. النشر التلقائي
4. تشغيل `flask db upgrade` تلقائياً

## الميزات الأساسية المتاحة:

✅ **إدارة الشحنات:**
- إنشاء شحنات عامة ومستندات
- تتبع الشحنات بالخرائط
- طباعة الفواتير والملصقات

✅ **النظام المالي:**
- تتبع الإيرادات والمصروفات
- تقارير مالية شاملة
- حساب الأرباح والخسائر

✅ **إدارة المستخدمين:**
- نظام صلاحيات متقدم
- مشرف رئيسي ومستخدمين

✅ **التصميم المتجاوب:**
- واجهة عربية/إنجليزية
- تصميم متجاوب للجوال
- خرائط تفاعلية

## حالة الاستعداد للنشر: ✅ جاهز 100%

جميع الملفات المطلوبة موجودة ومعدة بشكل صحيح لنشر النظام على أي منصة تدعم PostgreSQL.