# نظام إدارة الشحن - نسخة PHP

## نظرة عامة

هذه هي النسخة المحولة من Python/Flask إلى PHP الخالص لنظام إدارة الشحن. تم تطوير هذه النسخة لحل مشاكل الاستضافة ولتوفير نظام أبسط وأكثر توافقاً مع خوادم الويب التقليدية.

## ✅ المميزات المكتملة

### 🔐 نظام المصادقة والأمان
- تسجيل دخول آمن مع حماية CSRF
- نظام صلاحيات متدرج
- تشفير كلمات المرور
- تسجيل العمليات (Activity Log)
- جلسات آمنة

### 📦 إدارة الشحنات
- إضافة شحنة جديدة مع جميع التفاصيل
- عرض وفلترة الشحنات
- البحث في الشحنات
- تحديث حالة الشحنات
- طباعة الفواتير
- تتبع المدفوعات والمبالغ المتبقية

### 🌍 دعم متعدد اللغات
- واجهة عربية كاملة (RTL)
- دعم الإنجليزية
- تبديل سهل بين اللغات
- ترجمة ديناميكية للنصوص

### 💼 لوحة التحكم
- إحصائيات شاملة
- الشحنات الأخيرة
- روابط سريعة
- واجهة سريعة الاستجابة

### 📱 تصميم متجاوب
- يعمل على جميع الأجهزة
- تصميم Bootstrap محسن
- واجهة سهلة الاستخدام
- دعم الهواتف المحمولة

## 🏗️ هيكل المشروع

```
php_version/
├── config/
│   ├── config.php          # إعدادات النظام العامة
│   └── database.php        # إعدادات قاعدة البيانات
├── models/
│   ├── Shipment.php        # نموذج الشحنات
│   └── User.php            # نموذج المستخدمين
├── views/
│   ├── header.php          # رأس الصفحة
│   └── footer.php          # ذيل الصفحة
├── includes/
│   ├── functions.php       # الدوال المساعدة
│   └── translations.php    # نظام الترجمة
├── assets/
│   ├── css/               # ملفات التنسيق
│   ├── js/                # ملفات JavaScript
│   └── images/            # الصور
├── index.php              # الصفحة الرئيسية
├── login.php              # صفحة تسجيل الدخول
├── add_shipment.php       # إضافة شحنة جديدة
├── shipments.php          # عرض الشحنات
├── setup.php              # إعداد النظام
└── logout.php             # تسجيل الخروج
```

## 🚀 التثبيت والإعداد

### المتطلبات الأساسية
- PHP 8.0 أو أحدث
- MySQL 5.7 أو أحدث
- خادم ويب (Apache/Nginx)
- امتداد PDO MySQL

### خطوات التثبيت

#### 1. رفع الملفات
```bash
# ارفع جميع ملفات php_version إلى خادمك
# تأكد من أن مجلد uploads قابل للكتابة
chmod 755 uploads/
```

#### 2. إعداد قاعدة البيانات
```sql
-- إنشاء قاعدة البيانات
CREATE DATABASE shipping_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- إنشاء مستخدم (اختياري)
CREATE USER 'shipping_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON shipping_system.* TO 'shipping_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. تحديث إعدادات قاعدة البيانات
```php
// في config/config.php
define('DB_HOST', 'localhost');
define('DB_NAME', 'shipping_system');
define('DB_USER', 'shipping_user');
define('DB_PASS', 'password123');
```

#### 4. تشغيل الإعداد الأولي
```
https://yourdomain.com/shipping/setup.php
```

#### 5. تسجيل الدخول
```
اسم المستخدم: admin
كلمة المرور: admin123
```

## 🔧 التكوين المتقدم

### إعدادات الأمان
```php
// في config/config.php
define('SECRET_KEY', 'your-unique-secret-key-here');
```

### إعدادات الرفع
```php
define('MAX_UPLOAD_SIZE', 16777216); // 16MB
define('UPLOAD_PATH', __DIR__ . '/../uploads/');
```

### إعدادات اللغة
```php
define('DEFAULT_LANGUAGE', 'ar'); // ar للعربية، en للإنجليزية
```

## 📊 قاعدة البيانات

### الجداول الرئيسية

#### admin - المستخدمين الإداريين
```sql
- id: المعرف الفريد
- username: اسم المستخدم
- email: البريد الإلكتروني
- password_hash: كلمة المرور المشفرة
- is_super_admin: مدير عام
- permissions: الصلاحيات (JSON)
- last_login: آخر تسجيل دخول
- created_at: تاريخ الإنشاء
```

#### shipment - الشحنات
```sql
- id: المعرف الفريد
- tracking_number: رقم التتبع
- sender_name: اسم المرسل
- sender_phone: هاتف المرسل
- sender_address: عنوان المرسل
- receiver_name: اسم المستلم
- receiver_phone: هاتف المستلم
- receiver_address: عنوان المستلم
- weight: الوزن
- price: السعر
- paid_amount: المبلغ المدفوع
- remaining_amount: المبلغ المتبقي
- package_contents: محتويات الطرد
- package_type: نوع الطرد
- shipping_method: طريقة الشحن
- zone: المنطقة
- status: الحالة
- created_at: تاريخ الإنشاء
```

#### activity_log - سجل العمليات
```sql
- id: المعرف الفريد
- user_id: معرف المستخدم
- action: نوع العملية
- details: تفاصيل العملية
- ip_address: عنوان IP
- user_agent: معلومات المتصفح
- created_at: تاريخ العملية
```

## 🎨 التخصيص

### إضافة صفحة جديدة
```php
<?php
require_once 'config/config.php';
requireLogin();
// إضافة التحقق من الصلاحيات إذا لزم الأمر
// requirePermission('page_name');

$pageTitle = 'عنوان الصفحة';
include 'views/header.php';
?>

<!-- محتوى الصفحة هنا -->

<?php include 'views/footer.php'; ?>
```

### إضافة صلاحية جديدة
```php
// في نموذج المستخدم
$permissions = [
    'home', 'shipments', 'tracking', 
    'reports', 'expenses', 'add_shipment', 
    'settings', 'new_permission'
];
```

### تخصيص التصميم
```css
/* في assets/css/custom.css */
.custom-style {
    /* أضف أنماطك المخصصة هنا */
}
```

## 🔒 الأمان

### الممارسات الآمنة المطبقة
- تشفير كلمات المرور باستخدام password_hash()
- حماية من CSRF attacks
- تنظيف المدخلات (Input Sanitization)
- استعلامات SQL محضرة (Prepared Statements)
- التحقق من الصلاحيات على كل صفحة
- تسجيل العمليات الحساسة

### توصيات أمنية إضافية
- تغيير كلمة مرور المدير الافتراضية
- استخدام HTTPS في الإنتاج
- تحديث PHP إلى أحدث إصدار
- تفعيل جدار الحماية
- عمل نسخ احتياطية دورية

## 🐛 حل المشاكل الشائعة

### خطأ الاتصال بقاعدة البيانات
```
تحقق من:
- معلومات الاتصال في config/config.php
- تشغيل خدمة MySQL
- صلاحيات المستخدم
```

### صفحة بيضاء أو خطأ 500
```
تحقق من:
- error_log في cPanel أو /var/log/apache2/
- إعدادات PHP
- أذونات الملفات والمجلدات
```

### مشاكل الترميز العربي
```
تحقق من:
- تعيين UTF-8 في قاعدة البيانات
- headers في PHP
- meta charset في HTML
```

## 📈 التطوير المستقبلي

### المميزات المخططة
- [ ] نظام التتبع المتقدم
- [ ] تقارير مالية مفصلة
- [ ] إشعارات SMS
- [ ] تكامل مع API خارجية
- [ ] تطبيق الهاتف المحمول
- [ ] نظام الفواتير الإلكترونية

### كيفية المساهمة
1. Fork المشروع
2. إنشاء فرع للميزة الجديدة
3. تنفيذ التغييرات
4. إضافة اختبارات
5. إرسال Pull Request

## 📞 الدعم

### الحصول على المساعدة
- مراجعة هذا الدليل أولاً
- فحص ملفات السجلات
- التحقق من إعدادات قاعدة البيانات
- مراجعة أذونات الملفات

### معلومات النظام
- **الإصدار**: 2.0.0
- **اللغة**: PHP 8.0+
- **قاعدة البيانات**: MySQL 5.7+
- **Frontend**: Bootstrap 5.3
- **الترخيص**: MIT

---

## ✅ مقارنة مع النسخة السابقة (Python)

| الميزة | Python/Flask | PHP |
|--------|-------------|-----|
| سهولة النشر | ❌ معقد | ✅ بسيط |
| متطلبات الخادم | ❌ Python + مكتبات | ✅ PHP فقط |
| الأداء | ✅ سريع | ✅ سريع |
| سهولة التطوير | ✅ ممتاز | ✅ ممتاز |
| دعم الاستضافة | ❌ محدود | ✅ واسع |
| التكلفة | ❌ أعلى | ✅ أقل |

**النتيجة: النسخة PHP أبسط في النشر والصيانة مع نفس الوظائف**

---

🎉 **النظام جاهز للاستخدام الفوري!**