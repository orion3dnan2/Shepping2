# مرسال إكسبرس للاستيراد والتصدير - Shipping Management System

## نظرة عامة

نظام إدارة شحنات شامل مبني بـ Flask مع قاعدة بيانات PostgreSQL، يوفر إدارة الشحنات، التتبع الجغرافي، والتقارير المالية المتكاملة.

## المتطلبات التقنية

- Python 3.11+
- PostgreSQL 13+
- Flask 3.1+
- إنترنت للمكتبات الخارجية (Bootstrap, Font Awesome)

## إعداد المشروع

### 1. إعداد قاعدة البيانات

```bash
# إنشاء قاعدة بيانات PostgreSQL
createdb shipment_db

# تعيين متغير البيئة
export DATABASE_URL="postgresql://username:password@localhost:5432/shipment_db"
```

### 2. تثبيت التبعيات

```bash
pip install -r requirements.txt
# أو إذا كنت تستخدم uv
uv sync
```

### 3. تهيئة قاعدة البيانات

```bash
# تهيئة migrations
flask db init

# إنشاء migration أولي
flask db migrate -m "Initial migration"

# تطبيق migrations
flask db upgrade
```

### 4. تشغيل التطبيق

#### بيئة التطوير:
```bash
python main.py
```

#### بيئة الإنتاج:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

## متغيرات البيئة المطلوبة

```env
DATABASE_URL=postgresql://user:password@host:port/database
SESSION_SECRET=your-secret-key-here
FLASK_ENV=production
```

## ترحيل البيانات من SQLite

إذا كان لديك بيانات في SQLite وتريد ترحيلها:

### 1. تصدير البيانات من SQLite:

```bash
# إنشاء ملف SQL backup
sqlite3 shipments.db .dump > sqlite_backup.sql
```

### 2. تحويل تنسيق البيانات:

```bash
# إزالة SQLite-specific syntax
sed -i 's/autoincrement//' sqlite_backup.sql
sed -i 's/INTEGER PRIMARY KEY/SERIAL PRIMARY KEY/g' sqlite_backup.sql
```

### 3. استيراد إلى PostgreSQL:

```bash
# تنظيف قاعدة البيانات أولاً (احذر: سيحذف جميع البيانات)
flask db downgrade base
flask db upgrade

# استيراد البيانات
psql $DATABASE_URL < sqlite_backup.sql
```

## هيكل المشروع

```
project/
├── app.py                 # إعداد Flask الأساسي
├── main.py               # نقطة دخول التطبيق
├── models.py             # نماذج قاعدة البيانات
├── routes.py             # مسارات التطبيق
├── translations.py       # ملف الترجمة
├── templates/            # قوالب HTML
├── static/              # ملفات CSS/JS/الصور
├── migrations/          # ملفات ترحيل قاعدة البيانات
├── Procfile            # إعداد النشر للمنصات السحابية
├── .flaskenv           # متغيرات بيئة Flask
└── pyproject.toml      # تبعيات Python
```

## الميزات الرئيسية

### 1. إدارة الشحنات
- إنشاء وتعديل الشحنات
- أرقام تتبع فريدة
- تتبع الحالة المتقدم

### 2. النظام المالي
- تتبع الإيرادات والمصروفات
- تقارير مالية شاملة
- حساب الأرباح والخسائر

### 3. المستخدمين والصلاحيات
- نظام مستخدمين متقدم
- صلاحيات مبنية على الأدوار
- إدارة المشرف الرئيسي

### 4. التتبع الجغرافي
- خرائط تفاعلية
- تتبع المواقع
- مسار الشحنة المرئي

## نشر التطبيق

### Render.com

1. أربط المستودع بـ Render
2. تأكد من وجود Procfile
3. أضف متغيرات البيئة في لوحة التحكم
4. انشر التطبيق

### Heroku

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SESSION_SECRET=your-secret-key
git push heroku main
heroku run flask db upgrade
```

### Railway

1. أربط المستودع مع Railway
2. أضف خدمة PostgreSQL
3. أضف متغيرات البيئة
4. انشر التطبيق

## أمان قاعدة البيانات

### 1. النسخ الاحتياطي:

```bash
# نسخة احتياطية يومية
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### 2. مراقبة الأداء:

```sql
-- عرض الاستعلامات البطيئة
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

## التحسينات المطبقة لـ PostgreSQL

### 1. استخدام JSONB للبيانات المنظمة:
- حقل `permissions` في جدول `admin`
- فهرسة سريعة للبيانات JSON

### 2. Connection Pooling:
- `pool_size`: 10 اتصالات
- `max_overflow`: 20 اتصال إضافي
- `pool_recycle`: 300 ثانية

### 3. تحسين الاستعلامات:
- فهارس على الحقول المهمة
- استعلامات محسنة للتقارير

## دعم اللغات

التطبيق يدعم:
- العربية (الافتراضي)
- الإنجليزية
- تبديل اللغة في الوقت الفعلي

## المساعدة والدعم

### المشاكل الشائعة:

1. **خطأ في الاتصال بقاعدة البيانات:**
   - تأكد من صحة DATABASE_URL
   - تأكد من تشغيل PostgreSQL

2. **مشكلة في Migration:**
   ```bash
   flask db stamp head
   flask db migrate
   flask db upgrade
   ```

3. **مشكلة في الصلاحيات:**
   - اتصل كمشرف رئيسي (admin/admin123)
   - قم بتعديل الصلاحيات من الإعدادات

## المساهمة

للمساهمة في تطوير النظام:
1. فرع المستودع
2. أنشئ branch جديد للميزة
3. اكتب الكود مع التوثيق
4. أرسل Pull Request

## الترخيص

هذا المشروع مرخص لـ مرسال إكسبرس للاستيراد والتصدير.