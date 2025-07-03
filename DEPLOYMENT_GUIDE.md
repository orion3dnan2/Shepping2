# دليل الاستضافة على Render

## خطوات الاستضافة:

### 1. إعداد المشروع على GitHub
```bash
# إنشاء مستودع جديد على GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/shipping-management.git
git push -u origin main
```

### 2. إنشاء حساب على Render
- اذهب إلى https://render.com
- أنشئ حساب جديد أو سجل الدخول
- اربط حسابك بـ GitHub

### 3. إنشاء قاعدة البيانات
- في لوحة التحكم، اضغط على "New MySQL"
- أدخل الاسم: `shipping-database`
- اختر الخطة المجانية
- اضغط "Create Database"
- احفظ رابط قاعدة البيانات (DATABASE_URL)
- تأكد أن الرابط يبدأ بـ `mysql://`

### 4. إنشاء الخدمة الرئيسية
- اضغط على "New Web Service"
- اختر مستودع GitHub الخاص بك
- أدخل المعلومات التالية:
  - **Name**: `shipping-management-system`
  - **Environment**: `Python 3`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`

### 5. تكوين متغيرات البيئة
في قسم Environment Variables، أضف:
```
DATABASE_URL = [رابط قاعدة البيانات من الخطوة 3]
SESSION_SECRET = [مفتاح عشوائي آمن]
FLASK_ENV = production
```

### 6. نشر التطبيق
- اضغط "Create Web Service"
- انتظر حتى يكتمل النشر (5-10 دقائق)
- ستحصل على رابط التطبيق: `https://your-app-name.onrender.com`

## البيانات الافتراضية:
- **اسم المستخدم**: admin
- **كلمة المرور**: admin123

## نصائح مهمة:
1. استخدم خطة مدفوعة لتطبيقات الإنتاج
2. احفظ نسخة احتياطية من قاعدة البيانات بانتظام
3. قم بتحديث كلمة مرور الإدارة بعد النشر
4. راقب استخدام الموارد والأداء

## استكشاف الأخطاء:
- تحقق من logs في لوحة التحكم
- تأكد من صحة متغيرات البيئة
- تحقق من اتصال قاعدة البيانات