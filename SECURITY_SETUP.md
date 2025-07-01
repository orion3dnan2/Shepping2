# دليل إعداد الأمان لنظام مرسال إكسبرس
## Security Setup Guide for Morsal Express System

## 🔐 إعدادات متغيرات البيئة المطلوبة (Required Environment Variables)

### للإنتاج (Production Environment):
```bash
# إعدادات قاعدة البيانات الآمنة
export DATABASE_URL="postgresql://username:password@host:port/database_name"

# مفتاح جلسة آمن (يجب إنشاؤه عشوائياً)
export SESSION_SECRET="your-super-secure-session-secret-key-here-64-characters-minimum"

# تحديد بيئة الإنتاج
export ENVIRONMENT="production"

# إعدادات الأمان الإضافية
export FLASK_ENV="production"
export FLASK_DEBUG="False"
```

### لإنشاء مفتاح جلسة آمن:
```bash
# استخدم أحد الأوامر التالية لإنشاء مفتاح آمن
python -c "import secrets; print(secrets.token_hex(32))"
# أو
openssl rand -hex 32
```

## 🛡️ الميزات الأمنية المطبقة (Implemented Security Features)

### ✅ 1. Flask-Login Protection
- حماية جميع صفحات لوحة التحكم
- منع الوصول للمستخدمين غير المسجلين
- إدارة جلسات آمنة مع انتهاء صلاحية

### ✅ 2. تشفير كلمات المرور (Password Encryption)
- استخدام bcrypt للتشفير المتقدم
- الحد الأدنى 8 أحرف لكلمة المرور
- عدم حفظ أي كلمة مرور بنص صريح

### ✅ 3. حماية CSRF (CSRF Protection)
- حماية جميع النماذج باستخدام Flask-WTF
- انتهاء صلاحية tokens كل ساعة
- معالجة أخطاء CSRF بأمان

### ✅ 4. فلترة البيانات (Input Validation & Sanitization)
- فلترة جميع المدخلات لمنع XSS
- تحقيق صحة البيانات باستخدام WTForms
- حماية من SQL Injection عبر SQLAlchemy ORM
- تشفير النصوص في العرض

### ✅ 5. أمان الإنتاج (Production Security)
- تعطيل debug mode في الإنتاج
- إخفاء رسائل الخطأ التقنية
- صفحات خطأ مخصصة (404, 500, 403)

### ✅ 6. حماية متغيرات البيئة (Environment Variables)
- استخدام متغيرات بيئة لجميع البيانات الحساسة
- فحص وجود متغيرات الأمان المطلوبة
- رسائل تحذير في بيئة التطوير

### ✅ 7. إخفاء رسائل الخطأ (Error Handling)
- صفحات خطأ مخصصة للمستخدمين
- تسجيل مفصل للأخطاء للمطورين
- عدم كشف معلومات النظام

### ✅ 8. فحص الملفات المرفقة (File Upload Security)
- التحقق من أنواع الملفات المسموحة
- فحص حجم الملفات (حد أقصى 10 ميجابايت)
- التحقق من digital signatures للملفات
- منع الملفات الضارة

### ✅ 9. ميزات أمان إضافية (Additional Security Features)
- Rate limiting لمنع هجمات brute force
- تسجيل محاولات تسجيل الدخول
- حماية من Open Redirect attacks
- تشفير IP addresses في logs

## 🚀 خطوات النشر الآمن (Secure Deployment Steps)

### 1. إعداد قاعدة البيانات:
```bash
# إنشاء قاعدة بيانات PostgreSQL آمنة
createdb morsal_production
# تعيين مستخدم بصلاحيات محدودة
createuser --no-superuser --no-createdb --no-createrole morsal_user
```

### 2. تعيين متغيرات البيئة:
```bash
# إضافة المتغيرات لملف .env في الإنتاج
echo "DATABASE_URL=postgresql://morsal_user:password@localhost/morsal_production" >> .env
echo "SESSION_SECRET=$(openssl rand -hex 32)" >> .env
echo "ENVIRONMENT=production" >> .env
```

### 3. تشغيل النظام:
```bash
# تشغيل مع Gunicorn للإنتاج
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

## 🔍 فحص الأمان (Security Checklist)

- [ ] تم تعيين SESSION_SECRET كمتغير بيئة
- [ ] تم تعيين DATABASE_URL بشكل آمن
- [ ] تم تعطيل debug mode (ENVIRONMENT=production)
- [ ] تم تغيير كلمة مرور المدير الافتراضية
- [ ] تم فحص جميع النماذج للحماية من CSRF
- [ ] تم تطبيق Rate limiting على تسجيل الدخول
- [ ] تم إعداد SSL/HTTPS للإنتاج
- [ ] تم إعداد جدار حماية (Firewall)
- [ ] تم إعداد backup منتظم لقاعدة البيانات

## 📝 ملاحظات هامة (Important Notes)

1. **لا تضع أي معلومات حساسة في الكود**: استخدم متغيرات البيئة دائماً
2. **غيّر كلمة المرور الافتراضية**: المستخدم الافتراضي admin/admin123 يجب تغييره
3. **استخدم HTTPS في الإنتاج**: للحماية من التنصت على البيانات
4. **راقب logs الأمان**: لاكتشاف محاولات الاختراق
5. **حديث النظام بانتظام**: للحصول على آخر تحديثات الأمان

## 🆘 في حالة مشاكل الأمان (Security Issues)

إذا واجهت أي مشاكل أمنية:
1. راجع logs النظام
2. تأكد من إعداد متغيرات البيئة
3. فحص صلاحيات قاعدة البيانات
4. تأكد من تحديث جميع المكتبات