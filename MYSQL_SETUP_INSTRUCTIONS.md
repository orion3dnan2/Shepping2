# تعليمات إعداد MySQL للمشروع

## التحديثات المكتملة ✅

تم تحديث المشروع بنجاح ليعتمد على MySQL فقط:

### 1. إزالة دعم SQLite
- ✅ تم حذف جميع إعدادات SQLite من `app.py`
- ✅ تم حذف مجلد `instance/` وملفات قاعدة البيانات المحلية
- ✅ تم تنظيف الكود ليعتمد على MySQL فقط

### 2. تحديث إعدادات قاعدة البيانات
- ✅ تم تحديث `app.py` لاستخدام MySQL فقط
- ✅ تم إزالة `psycopg2-binary` من `pyproject.toml`
- ✅ تم الاحتفاظ بـ `pymysql` كمحرك قاعدة البيانات

### 3. إعدادات MySQL الجديدة
```python
# في app.py
mysql_url = os.environ.get("MYSQL_DATABASE_URL") or "mysql+pymysql://root:password123@localhost:3306/shipping_db"
```

## كيفية الاستخدام مع MySQL

### للتطوير المحلي:
```bash
export MYSQL_DATABASE_URL="mysql+pymysql://username:password@localhost:3306/shipping_db"
```

### للإنتاج (cPanel):
```bash
export MYSQL_DATABASE_URL="mysql+pymysql://username:password@hostname:3306/database_name"
```

## إعدادات MySQL المطلوبة

### 1. إنشاء قاعدة البيانات
```sql
CREATE DATABASE shipping_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. إنشاء مستخدم (اختياري)
```sql
CREATE USER 'shipping_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON shipping_db.* TO 'shipping_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. تحديث معلومات الاتصال
```python
# في production
MYSQL_DATABASE_URL = "mysql+pymysql://shipping_user:secure_password@localhost:3306/shipping_db"
```

## الملاحظات المهمة

- 🔒 **الأمان**: تغيير كلمة المرور الافتراضية في الإنتاج
- 🗃️ **الترميز**: استخدام `utf8mb4` لدعم الأحرف العربية
- 📊 **الأداء**: تم تحسين إعدادات connection pool لـ MySQL
- 🔧 **الصيانة**: جميع النماذج متوافقة مع MySQL

## حالة المشروع

✅ **مكتمل**: المشروع يعمل الآن مع MySQL فقط
✅ **تم الاختبار**: التطبيق يتعرف على إعدادات MySQL
✅ **جاهز للإنتاج**: يمكن نشر المشروع على cPanel مع MySQL

---

**ملاحظة**: لتشغيل التطبيق بشكل كامل، تحتاج إلى إعداد خادم MySQL وإنشاء قاعدة البيانات المطلوبة.