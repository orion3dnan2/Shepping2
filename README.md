# نظام إدارة الشحن - دليل شامل للمطورين

## 🎯 نظرة عامة على النظام

نظام إدارة الشحن هو تطبيق ويب شامل مبني بـ Flask لإدارة عمليات الشحن بين الكويت والسودان. يتضمن النظام إدارة الشحنات، تتبع الطرود، المعاملات المالية، وإدارة المستخدمين مع دعم كامل للغة العربية.

### المزايا الرئيسية:
- **إدارة الشحنات**: إنشاء وتتبع وإدارة الشحنات
- **الإدارة المالية**: تتبع الإيرادات والمصروفات والأرباح
- **تتبع الطرود**: تتبع عام ومحدود للشحنات
- **إدارة المستخدمين**: نظام صلاحيات متقدم
- **دعم ثنائي اللغة**: العربية والإنجليزية
- **تصميم متجاوب**: يعمل على الهاتف والحاسوب

---

## 🏗️ البنية التقنية

### Frontend
- **Framework**: Bootstrap 5.3.0 مع تصميم مخصص
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Tajawal, Cairo) للنصوص العربية
- **JavaScript**: Vanilla JS للتفاعل
- **RTL Support**: دعم كامل للنصوص من اليمين لليسار

### Backend
- **Framework**: Flask 3.1.1 (Python)
- **Database**: SQLAlchemy ORM مع PostgreSQL/MySQL
- **Authentication**: Flask-Login
- **Templates**: Jinja2 مع Bootstrap
- **WSGI**: Gunicorn للإنتاج

### قاعدة البيانات
- **الجداول**: 16 جدول أساسي
- **العلاقات**: Foreign Keys مع CASCADE
- **المحتوى**: بيانات أساسية باللغة العربية والإنجليزية

---

## 📂 بنية الملفات

```
/
├── app.py                 # تطبيق Flask الرئيسي
├── main.py               # نقطة الدخول
├── models.py             # نماذج قاعدة البيانات
├── routes.py             # معالجات الطلبات
├── translations.py       # الترجمات العربية/الإنجليزية
├── passenger_wsgi.py     # WSGI للاستضافة
├── .htaccess            # إعدادات Apache
├── requirements.txt     # المكتبات المطلوبة
├── database_schema.sql  # هيكل قاعدة البيانات
├── database_init.sql    # البيانات الأولية
├── static/              # الملفات الثابتة
│   ├── css/
│   │   └── style.css    # التصميم الرئيسي
│   ├── js/
│   │   └── main.js      # الوظائف التفاعلية
│   ├── images/          # الصور والأيقونات
│   └── fonts/           # الخطوط المخصصة
├── templates/           # قوالب HTML
│   ├── base.html        # القالب الأساسي
│   ├── index.html       # الصفحة الرئيسية
│   ├── login.html       # صفحة تسجيل الدخول
│   ├── shipments/       # صفحات الشحنات
│   ├── financial/       # صفحات المالية
│   └── settings/        # صفحات الإعدادات
└── instance/            # بيانات التطبيق
```

---

## 🗄️ هيكل قاعدة البيانات

### الجداول الرئيسية:

#### 1. admin - المشرفين
```sql
- id (Primary Key)
- username (unique)
- password_hash (scrypt)
- permissions (JSON)
- is_super_admin (boolean)
- created_at (timestamp)
```

#### 2. shipment - الشحنات
```sql
- id (Primary Key)
- tracking_number (unique, SHIP-YYYYMMDD-XXX)
- sender_name, sender_phone, sender_address, sender_email
- receiver_name, receiver_phone, receiver_address, receiver_email
- direction (kuwait_to_sudan/sudan_to_kuwait)
- package_type (general/document)
- shipping_method (جوي/بري)
- weight (float)
- zone (نطاق التسعير)
- price, cost, profit (مالية)
- status (created/in_transit/delivered/cancelled)
- confirmed (boolean)
- created_at (timestamp)
```

#### 3. shipment_type - أنواع الشحن
```sql
- id (Primary Key)
- name_ar, name_en
- price (float)
- is_active (boolean)
- created_at (timestamp)
```

#### 4. document_type - أنواع الوثائق
```sql
- id (Primary Key)
- name_ar, name_en (توثيق خارجية، شهادات، إلخ)
- price (float)
- is_active (boolean)
- created_at (timestamp)
```

#### 5. zone_pricing - نطاقات التسعير
```sql
- id (Primary Key)
- zone_name_ar, zone_name_en
- price_per_kg (float)
- direction (kuwait_to_sudan/sudan_to_kuwait)
- is_active (boolean)
- created_at (timestamp)
```

#### 6. financial_transaction - المعاملات المالية
```sql
- id (Primary Key)
- name (اسم المعاملة)
- amount (float)
- transaction_type (expense/revenue)
- category (تصنيف)
- transaction_date (timestamp)
- created_at (timestamp)
```

#### 7. notification - الإشعارات
```sql
- id (Primary Key)
- title, message
- tracking_number (optional)
- is_read (boolean)
- created_at (timestamp)
```

---

## 🎨 نظام التصميم

### الألوان الرئيسية:
```css
:root {
  --primary-color: #2c3e50;      /* الأزرق الداكن */
  --secondary-color: #3498db;     /* الأزرق الفاتح */
  --success-color: #27ae60;       /* الأخضر */
  --danger-color: #e74c3c;        /* الأحمر */
  --warning-color: #f39c12;       /* البرتقالي */
  --info-color: #17a2b8;          /* الأزرق الفاتح */
  --light-color: #f8f9fa;         /* الرمادي الفاتح */
  --dark-color: #343a40;          /* الرمادي الداكن */
}
```

### الخطوط:
```css
/* للنصوص العربية */
font-family: 'Tajawal', 'Cairo', sans-serif;

/* للنصوص الإنجليزية */
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### التصميم المتجاوب:
```css
/* الهاتف */
@media (max-width: 768px) {
  .container { padding: 10px; }
  .table-responsive { overflow-x: auto; }
}

/* الحاسوب */
@media (min-width: 992px) {
  .sidebar { width: 250px; }
  .main-content { margin-left: 250px; }
}
```

---

## 🔧 إعداد النظام

### 1. متطلبات التشغيل:
```bash
Python 3.8+
PostgreSQL 12+ أو MySQL 8+
```

### 2. المكتبات المطلوبة:
```bash
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.0.0
PyMySQL==1.1.1
psycopg2-binary==2.9.9
Werkzeug==3.1.3
Jinja2==3.1.6
```

### 3. متغيرات البيئة:
```bash
DATABASE_URL=postgresql://user:pass@localhost/shipping_db
SESSION_SECRET=your-secret-key-here
FLASK_ENV=production
```

### 4. إعداد قاعدة البيانات:
```sql
-- إنشاء قاعدة البيانات
CREATE DATABASE shipping_system;

-- استيراد الهيكل
\i database_schema.sql

-- إضافة البيانات الأولية
\i database_init.sql
```

---

## 🌐 صفحات النظام

### 1. الصفحة الرئيسية (/)
**الملف**: `templates/index.html`
**الوظائف**:
- عرض إحصائيات سريعة
- آخر الشحنات
- الإشعارات
- روابط سريعة

**المكونات**:
```html
<!-- بطاقات الإحصائيات -->
<div class="stats-cards">
  <div class="stat-card">
    <h3>{{ total_shipments }}</h3>
    <p>إجمالي الشحنات</p>
  </div>
</div>

<!-- جدول آخر الشحنات -->
<div class="recent-shipments">
  <table class="table">
    <!-- محتوى الجدول -->
  </table>
</div>
```

### 2. صفحة تسجيل الدخول (/login)
**الملف**: `templates/login.html`
**الوظائف**:
- تسجيل دخول المشرفين
- التحقق من كلمة المرور
- إعادة توجيه للصفحة الرئيسية

**النموذج**:
```html
<form method="POST" class="login-form">
  <div class="form-group">
    <label>اسم المستخدم</label>
    <input type="text" name="username" required>
  </div>
  <div class="form-group">
    <label>كلمة المرور</label>
    <input type="password" name="password" required>
  </div>
  <button type="submit">دخول</button>
</form>
```

### 3. إدارة الشحنات (/shipments)
**الملف**: `templates/shipments/index.html`
**الوظائف**:
- عرض جميع الشحنات
- البحث والتصفية
- تصدير البيانات
- روابط التعديل والحذف

**مكونات الصفحة**:
```html
<!-- شريط البحث -->
<div class="search-bar">
  <input type="text" id="search" placeholder="البحث...">
  <select id="status-filter">
    <option value="">جميع الحالات</option>
    <option value="created">منشأة</option>
    <option value="in_transit">في الطريق</option>
    <option value="delivered">تم التسليم</option>
  </select>
</div>

<!-- جدول الشحنات -->
<div class="table-responsive">
  <table class="table table-striped">
    <thead>
      <tr>
        <th>رقم التتبع</th>
        <th>المرسل</th>
        <th>المستقبل</th>
        <th>الحالة</th>
        <th>التاريخ</th>
        <th>الإجراءات</th>
      </tr>
    </thead>
    <tbody>
      {% for shipment in shipments %}
      <tr>
        <td>{{ shipment.tracking_number }}</td>
        <td>{{ shipment.sender_name }}</td>
        <td>{{ shipment.receiver_name }}</td>
        <td>
          <span class="badge badge-{{ get_status_class(shipment.status) }}">
            {{ translate_status(shipment.status) }}
          </span>
        </td>
        <td>{{ shipment.created_at.strftime('%Y-%m-%d') }}</td>
        <td>
          <a href="/shipments/{{ shipment.id }}/edit" class="btn btn-sm btn-primary">تعديل</a>
          <a href="/shipments/{{ shipment.id }}/delete" class="btn btn-sm btn-danger">حذف</a>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

### 4. إضافة شحنة جديدة (/add_shipment)
**الملف**: `templates/shipments/add.html`
**الوظائف**:
- نموذج إضافة شحنة شامل
- حساب السعر تلقائياً
- التحقق من البيانات
- إنشاء رقم تتبع

**النموذج الشامل**:
```html
<form method="POST" class="shipment-form">
  <!-- معلومات المرسل -->
  <div class="card">
    <div class="card-header">
      <h5>معلومات المرسل</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label>اسم المرسل *</label>
            <input type="text" name="sender_name" required>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label>هاتف المرسل *</label>
            <input type="tel" name="sender_phone" required>
          </div>
        </div>
      </div>
      <div class="form-group">
        <label>عنوان المرسل</label>
        <textarea name="sender_address" rows="2"></textarea>
      </div>
      <div class="form-group">
        <label>بريد المرسل</label>
        <input type="email" name="sender_email">
      </div>
    </div>
  </div>

  <!-- معلومات المستقبل -->
  <div class="card">
    <div class="card-header">
      <h5>معلومات المستقبل</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label>اسم المستقبل *</label>
            <input type="text" name="receiver_name" required>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label>هاتف المستقبل *</label>
            <input type="tel" name="receiver_phone" required>
          </div>
        </div>
      </div>
      <div class="form-group">
        <label>عنوان المستقبل</label>
        <textarea name="receiver_address" rows="2"></textarea>
      </div>
      <div class="form-group">
        <label>بريد المستقبل</label>
        <input type="email" name="receiver_email">
      </div>
    </div>
  </div>

  <!-- تفاصيل الشحنة -->
  <div class="card">
    <div class="card-header">
      <h5>تفاصيل الشحنة</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-4">
          <div class="form-group">
            <label>الاتجاه *</label>
            <select name="direction" required>
              <option value="kuwait_to_sudan">الكويت → السودان</option>
              <option value="sudan_to_kuwait">السودان → الكويت</option>
            </select>
          </div>
        </div>
        <div class="col-md-4">
          <div class="form-group">
            <label>نوع الشحنة *</label>
            <select name="package_type" required>
              <option value="general">شحن عام</option>
              <option value="document">وثائق</option>
            </select>
          </div>
        </div>
        <div class="col-md-4">
          <div class="form-group">
            <label>طريقة الشحن *</label>
            <select name="shipping_method" required>
              <option value="جوي">شحن جوي</option>
              <option value="بري">شحن بري</option>
            </select>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label>الوزن (كيلو) *</label>
            <input type="number" name="weight" step="0.1" required>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label>النطاق *</label>
            <select name="zone" required>
              {% for zone in zones %}
              <option value="{{ zone.id }}">{{ zone.zone_name_ar }} - {{ zone.price_per_kg }} د.ك/كيلو</option>
              {% endfor %}
            </select>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>محتويات الطرد</label>
        <textarea name="package_contents" rows="2"></textarea>
      </div>

      <div class="form-group">
        <label>ملاحظات</label>
        <textarea name="notes" rows="3"></textarea>
      </div>
    </div>
  </div>

  <!-- الخدمات الإضافية -->
  <div class="card">
    <div class="card-header">
      <h5>الخدمات الإضافية</h5>
    </div>
    <div class="card-body">
      <div class="form-check">
        <input type="checkbox" name="has_packaging" value="true">
        <label>خدمة التغليف (+{{ packaging_price }} د.ك)</label>
      </div>
      <div class="form-check">
        <input type="checkbox" name="has_policy" value="true">
        <label>خدمة البوليصة (+{{ policy_price }} د.ك)</label>
      </div>
      <div class="form-check">
        <input type="checkbox" name="has_comment" value="true">
        <label>خدمة التعليق (+{{ comment_price }} د.ك)</label>
      </div>
    </div>
  </div>

  <!-- التسعير -->
  <div class="card">
    <div class="card-header">
      <h5>التسعير</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-4">
          <div class="form-group">
            <label>السعر الأساسي</label>
            <input type="number" name="base_price" step="0.001" readonly>
          </div>
        </div>
        <div class="col-md-4">
          <div class="form-group">
            <label>السعر النهائي</label>
            <input type="number" name="price" step="0.001" required>
          </div>
        </div>
        <div class="col-md-4">
          <div class="form-group">
            <label>التكلفة</label>
            <input type="number" name="cost" step="0.001" required>
          </div>
        </div>
      </div>
    </div>
  </div>

  <button type="submit" class="btn btn-primary">إضافة الشحنة</button>
</form>
```

### 5. تتبع الشحنة (/track/<tracking_number>)
**الملف**: `templates/shipments/track.html`
**الوظائف**:
- عرض تفاصيل الشحنة
- تاريخ المعاملات
- خريطة الموقع
- طباعة الملصق

**محتوى الصفحة**:
```html
<div class="tracking-page">
  <!-- معلومات الشحنة -->
  <div class="shipment-info">
    <h2>تتبع الشحنة: {{ shipment.tracking_number }}</h2>
    <div class="status-badge">
      <span class="badge badge-{{ get_status_class(shipment.status) }}">
        {{ translate_status(shipment.status) }}
      </span>
    </div>
  </div>

  <!-- تفاصيل الشحنة -->
  <div class="row">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">معلومات المرسل</div>
        <div class="card-body">
          <p><strong>الاسم:</strong> {{ shipment.sender_name }}</p>
          <p><strong>الهاتف:</strong> {{ shipment.sender_phone }}</p>
          <p><strong>العنوان:</strong> {{ shipment.sender_address }}</p>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">معلومات المستقبل</div>
        <div class="card-body">
          <p><strong>الاسم:</strong> {{ shipment.receiver_name }}</p>
          <p><strong>الهاتف:</strong> {{ shipment.receiver_phone }}</p>
          <p><strong>العنوان:</strong> {{ shipment.receiver_address }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- تاريخ الشحنة -->
  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-date">{{ shipment.created_at.strftime('%Y-%m-%d %H:%M') }}</div>
      <div class="timeline-content">تم إنشاء الشحنة</div>
    </div>
    {% if shipment.status == 'in_transit' %}
    <div class="timeline-item">
      <div class="timeline-date">{{ shipment.updated_at.strftime('%Y-%m-%d %H:%M') }}</div>
      <div class="timeline-content">الشحنة في الطريق</div>
    </div>
    {% endif %}
  </div>

  <!-- أزرار الطباعة -->
  <div class="print-buttons">
    <button onclick="printLabel()" class="btn btn-primary">طباعة الملصق</button>
    <button onclick="printReceipt()" class="btn btn-secondary">طباعة الإيصال</button>
  </div>
</div>
```

### 6. المركز المالي (/financial_center)
**الملف**: `templates/financial/index.html`
**الوظائف**:
- إحصائيات مالية شاملة
- تقارير الأرباح والخسائر
- إدارة المصروفات
- تصدير التقارير

**مكونات الصفحة**:
```html
<!-- الإحصائيات السريعة -->
<div class="financial-stats">
  <div class="stat-card">
    <h3>{{ total_revenue }}</h3>
    <p>إجمالي الإيرادات</p>
  </div>
  <div class="stat-card">
    <h3>{{ total_expenses }}</h3>
    <p>إجمالي المصروفات</p>
  </div>
  <div class="stat-card">
    <h3>{{ net_profit }}</h3>
    <p>صافي الربح</p>
  </div>
</div>

<!-- تقرير الأرباح والخسائر -->
<div class="profit-loss-report">
  <h4>تقرير الأرباح والخسائر</h4>
  <div class="date-filter">
    <input type="date" id="start-date">
    <input type="date" id="end-date">
    <button onclick="generateReport()">إنشاء التقرير</button>
  </div>
  
  <div class="report-content">
    <!-- محتوى التقرير يتم تحديثه بـ JavaScript -->
  </div>
</div>

<!-- جدول المعاملات -->
<div class="transactions-table">
  <h4>المعاملات المالية</h4>
  <table class="table">
    <thead>
      <tr>
        <th>التاريخ</th>
        <th>الوصف</th>
        <th>النوع</th>
        <th>المبلغ</th>
      </tr>
    </thead>
    <tbody>
      {% for transaction in transactions %}
      <tr>
        <td>{{ transaction.transaction_date.strftime('%Y-%m-%d') }}</td>
        <td>{{ transaction.name }}</td>
        <td>
          <span class="badge badge-{{ 'success' if transaction.transaction_type == 'revenue' else 'danger' }}">
            {{ 'إيراد' if transaction.transaction_type == 'revenue' else 'مصروف' }}
          </span>
        </td>
        <td>{{ transaction.amount }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

### 7. الإعدادات (/settings)
**الملف**: `templates/settings/index.html`
**الوظائف**:
- إعدادات النظام العامة
- إدارة المستخدمين
- تسعير المناطق
- إعدادات الشحن

**صفحات الإعدادات**:
```html
<!-- التبويبات -->
<ul class="nav nav-tabs">
  <li class="nav-item">
    <a class="nav-link active" href="#general">الإعدادات العامة</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#users">المستخدمين</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#pricing">التسعير</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#shipping">الشحن</a>
  </li>
</ul>

<!-- محتوى التبويبات -->
<div class="tab-content">
  <div class="tab-pane active" id="general">
    <form method="POST" action="/settings/general">
      <div class="form-group">
        <label>اسم الشركة</label>
        <input type="text" name="company_name" value="{{ company_name }}">
      </div>
      <div class="form-group">
        <label>سعر التغليف</label>
        <input type="number" name="packaging_price" step="0.001" value="{{ packaging_price }}">
      </div>
      <div class="form-group">
        <label>سعر البوليصة</label>
        <input type="number" name="policy_price" step="0.001" value="{{ policy_price }}">
      </div>
      <button type="submit" class="btn btn-primary">حفظ</button>
    </form>
  </div>
  
  <div class="tab-pane" id="users">
    <!-- إدارة المستخدمين -->
    <div class="users-management">
      <button class="btn btn-primary" onclick="addUser()">إضافة مستخدم</button>
      <table class="table">
        <thead>
          <tr>
            <th>اسم المستخدم</th>
            <th>الصلاحيات</th>
            <th>تاريخ الإنشاء</th>
            <th>الإجراءات</th>
          </tr>
        </thead>
        <tbody>
          {% for user in users %}
          <tr>
            <td>{{ user.username }}</td>
            <td>
              {% if user.is_super_admin %}
              <span class="badge badge-primary">مشرف عام</span>
              {% else %}
              <span class="badge badge-secondary">مستخدم</span>
              {% endif %}
            </td>
            <td>{{ user.created_at.strftime('%Y-%m-%d') }}</td>
            <td>
              <button class="btn btn-sm btn-warning" onclick="editUser({{ user.id }})">تعديل</button>
              <button class="btn btn-sm btn-danger" onclick="deleteUser({{ user.id }})">حذف</button>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>
```

---

## 🔐 نظام الأمان والصلاحيات

### تسجيل الدخول:
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Admin.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')
```

### التحقق من الصلاحيات:
```python
def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            if not current_user.has_permission(permission):
                flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### استخدام الصلاحيات:
```python
@app.route('/shipments')
@require_permission('shipments')
def shipments():
    # محتوى الصفحة
    pass

@app.route('/financial_center')
@require_permission('financial_center')
def financial_center():
    # محتوى الصفحة
    pass
```

---

## 🎯 الوظائف الرئيسية

### 1. إنشاء رقم تتبع:
```python
@staticmethod
def generate_tracking_number():
    """إنشاء رقم تتبع فريد بصيغة SHIP-YYYYMMDD-XXX"""
    today = datetime.now().strftime('%Y%m%d')
    prefix = f"SHIP-{today}-"
    
    # البحث عن آخر رقم تتبع اليوم
    last_shipment = Shipment.query.filter(
        Shipment.tracking_number.like(f"{prefix}%")
    ).order_by(Shipment.id.desc()).first()
    
    if last_shipment:
        last_number = int(last_shipment.tracking_number.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:03d}"
```

### 2. حساب التكلفة:
```python
def calculate_shipping_cost(self):
    """حساب تكلفة الشحنة بناءً على الوزن والمنطقة"""
    if self.package_type == 'document':
        # تكلفة الوثائق ثابتة
        return DocumentType.query.filter_by(id=self.document_type).first().price
    
    # تكلفة الشحن العام
    zone = ZonePricing.query.filter_by(
        id=self.zone, 
        direction=self.direction
    ).first()
    
    base_cost = zone.price_per_kg * self.weight
    
    # إضافة تكلفة الخدمات
    if self.has_packaging:
        base_cost += GlobalSettings.get_setting('packaging_price')
    
    if self.has_policy:
        base_cost += GlobalSettings.get_setting('policy_price')
    
    if self.has_comment:
        base_cost += GlobalSettings.get_setting('comment_price')
    
    return base_cost
```

### 3. البحث والتصفية:
```python
@app.route('/shipments')
def shipments():
    # متغيرات البحث
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # بناء الاستعلام
    query = Shipment.query
    
    if search:
        query = query.filter(
            db.or_(
                Shipment.tracking_number.contains(search),
                Shipment.sender_name.contains(search),
                Shipment.receiver_name.contains(search)
            )
        )
    
    if status:
        query = query.filter(Shipment.status == status)
    
    if start_date:
        query = query.filter(Shipment.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    
    if end_date:
        query = query.filter(Shipment.created_at <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    shipments = query.order_by(Shipment.created_at.desc()).all()
    
    return render_template('shipments/index.html', shipments=shipments)
```

### 4. تصدير البيانات:
```python
@app.route('/export/shipments')
def export_shipments():
    """تصدير الشحنات إلى CSV"""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # كتابة الرؤوس
    writer.writerow(['رقم التتبع', 'المرسل', 'المستقبل', 'الوزن', 'السعر', 'التاريخ'])
    
    # كتابة البيانات
    shipments = Shipment.query.all()
    for shipment in shipments:
        writer.writerow([
            shipment.tracking_number,
            shipment.sender_name,
            shipment.receiver_name,
            shipment.weight,
            shipment.price,
            shipment.created_at.strftime('%Y-%m-%d')
        ])
    
    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='shipments.csv'
    )
```

---

## 📱 JavaScript والتفاعل

### 1. البحث الفوري:
```javascript
// البحث الفوري في الجداول
function setupLiveSearch() {
    const searchInput = document.getElementById('search');
    const table = document.querySelector('.shipments-table tbody');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}
```

### 2. حساب التكلفة التلقائي:
```javascript
function calculateShippingCost() {
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    const zoneSelect = document.getElementById('zone');
    const pricePerKg = parseFloat(zoneSelect.options[zoneSelect.selectedIndex].dataset.price) || 0;
    
    let totalCost = weight * pricePerKg;
    
    // إضافة تكلفة الخدمات
    if (document.getElementById('has_packaging').checked) {
        totalCost += parseFloat(document.getElementById('packaging_price').value) || 0;
    }
    
    if (document.getElementById('has_policy').checked) {
        totalCost += parseFloat(document.getElementById('policy_price').value) || 0;
    }
    
    if (document.getElementById('has_comment').checked) {
        totalCost += parseFloat(document.getElementById('comment_price').value) || 0;
    }
    
    document.getElementById('base_price').value = totalCost.toFixed(3);
    document.getElementById('price').value = totalCost.toFixed(3);
}

// ربط الأحداث
document.addEventListener('DOMContentLoaded', function() {
    const weightInput = document.getElementById('weight');
    const zoneSelect = document.getElementById('zone');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    [weightInput, zoneSelect, ...checkboxes].forEach(element => {
        element.addEventListener('change', calculateShippingCost);
    });
});
```

### 3. طباعة الملصقات:
```javascript
function printLabel() {
    const printContent = document.getElementById('label-content');
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <html>
        <head>
            <title>طباعة الملصق</title>
            <style>
                body { font-family: Arial, sans-serif; }
                .label { 
                    width: 10cm; 
                    height: 7cm; 
                    border: 1px solid #000; 
                    padding: 1cm;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                }
                .tracking-number { 
                    font-size: 24px; 
                    font-weight: bold; 
                    text-align: center;
                }
                .barcode { 
                    text-align: center; 
                    margin: 10px 0;
                }
                .addresses { 
                    font-size: 12px; 
                }
            </style>
        </head>
        <body>
            <div class="label">
                <div class="tracking-number">${tracking_number}</div>
                <div class="barcode">||||| |||| ||||| ||||</div>
                <div class="addresses">
                    <div><strong>من:</strong> ${sender_name}</div>
                    <div><strong>إلى:</strong> ${receiver_name}</div>
                    <div><strong>الوزن:</strong> ${weight} كيلو</div>
                </div>
            </div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}
```

### 4. تحديث الحالة:
```javascript
function updateShipmentStatus(shipmentId, newStatus) {
    fetch(`/shipments/${shipmentId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('خطأ في تحديث الحالة');
        }
    });
}
```

---

## 🎨 تخصيص التصميم

### 1. المتغيرات CSS:
```css
/* ملف: static/css/style.css */

/* المتغيرات الرئيسية */
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
    --info-color: #17a2b8;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
    --border-radius: 8px;
    --box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* الخطوط */
body {
    font-family: 'Tajawal', 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

/* الشريط الجانبي */
.sidebar {
    width: 250px;
    height: 100vh;
    background: var(--primary-color);
    color: white;
    position: fixed;
    right: 0;
    top: 0;
    z-index: 1000;
    transition: all 0.3s ease;
}

.sidebar.collapsed {
    width: 60px;
}

.sidebar-header {
    padding: 20px;
    background: var(--dark-color);
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-menu {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar-menu li {
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-menu a {
    display: block;
    padding: 15px 20px;
    color: white;
    text-decoration: none;
    transition: background 0.3s ease;
}

.sidebar-menu a:hover {
    background: rgba(255,255,255,0.1);
}

.sidebar-menu a.active {
    background: var(--secondary-color);
}

/* المحتوى الرئيسي */
.main-content {
    margin-right: 250px;
    min-height: 100vh;
    background: #f8f9fa;
    transition: margin-right 0.3s ease;
}

.main-content.expanded {
    margin-right: 60px;
}

/* الشريط العلوي */
.top-bar {
    background: white;
    padding: 15px 30px;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--box-shadow);
}

.breadcrumb {
    background: none;
    padding: 0;
    margin: 0;
}

.user-menu {
    display: flex;
    align-items: center;
    gap: 15px;
}

.notifications {
    position: relative;
}

.notifications .badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: var(--danger-color);
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* البطاقات */
.card {
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    margin-bottom: 20px;
    overflow: hidden;
}

.card-header {
    background: var(--light-color);
    padding: 15px 20px;
    border-bottom: 1px solid #dee2e6;
    font-weight: bold;
}

.card-body {
    padding: 20px;
}

/* بطاقات الإحصائيات */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    padding: 30px;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    text-align: center;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--primary-color);
}

.stat-card.success::before {
    background: var(--success-color);
}

.stat-card.warning::before {
    background: var(--warning-color);
}

.stat-card.danger::before {
    background: var(--danger-color);
}

.stat-card h3 {
    font-size: 2.5rem;
    margin: 0;
    color: var(--primary-color);
}

.stat-card p {
    margin: 10px 0 0;
    color: #666;
}

/* الجداول */
.table-container {
    background: white;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--box-shadow);
}

.table {
    margin: 0;
}

.table thead th {
    background: var(--light-color);
    border-bottom: 2px solid #dee2e6;
    font-weight: bold;
    padding: 15px;
}

.table tbody td {
    padding: 15px;
    border-bottom: 1px solid #dee2e6;
}

.table tbody tr:hover {
    background: rgba(52, 144, 220, 0.1);
}

/* الأزرار */
.btn {
    padding: 10px 20px;
    border-radius: var(--border-radius);
    border: none;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: #1a252f;
}

.btn-success {
    background: var(--success-color);
    color: white;
}

.btn-success:hover {
    background: #1e8449;
}

.btn-warning {
    background: var(--warning-color);
    color: white;
}

.btn-warning:hover {
    background: #d35400;
}

.btn-danger {
    background: var(--danger-color);
    color: white;
}

.btn-danger:hover {
    background: #c0392b;
}

/* النماذج */
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: var(--dark-color);
}

.form-control {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid #dee2e6;
    border-radius: var(--border-radius);
    font-size: 14px;
    transition: border-color 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 2px rgba(52, 144, 220, 0.2);
}

.form-control.is-invalid {
    border-color: var(--danger-color);
}

.invalid-feedback {
    display: block;
    color: var(--danger-color);
    font-size: 12px;
    margin-top: 5px;
}

/* الشارات */
.badge {
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.badge-primary {
    background: var(--primary-color);
    color: white;
}

.badge-success {
    background: var(--success-color);
    color: white;
}

.badge-warning {
    background: var(--warning-color);
    color: white;
}

.badge-danger {
    background: var(--danger-color);
    color: white;
}

.badge-info {
    background: var(--info-color);
    color: white;
}

/* الرسائل */
.alert {
    padding: 15px;
    margin-bottom: 20px;
    border-radius: var(--border-radius);
    border: 1px solid transparent;
}

.alert-success {
    background: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
}

.alert-danger {
    background: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
}

.alert-warning {
    background: #fff3cd;
    border-color: #ffeaa7;
    color: #856404;
}

.alert-info {
    background: #d1ecf1;
    border-color: #bee5eb;
    color: #0c5460;
}

/* التصميم المتجاوب */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(100%);
    }
    
    .sidebar.show {
        transform: translateX(0);
    }
    
    .main-content {
        margin-right: 0;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .table-responsive {
        overflow-x: auto;
    }
    
    .top-bar {
        padding: 10px 15px;
    }
    
    .card-body {
        padding: 15px;
    }
}

/* التحريكات */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.3s ease;
}

/* التخصيصات الإضافية */
.text-primary { color: var(--primary-color) !important; }
.text-success { color: var(--success-color) !important; }
.text-warning { color: var(--warning-color) !important; }
.text-danger { color: var(--danger-color) !important; }
.text-info { color: var(--info-color) !important; }

.bg-primary { background: var(--primary-color) !important; }
.bg-success { background: var(--success-color) !important; }
.bg-warning { background: var(--warning-color) !important; }
.bg-danger { background: var(--danger-color) !important; }
.bg-info { background: var(--info-color) !important; }

/* التحسينات الخاصة */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

.spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

---

## 🚀 إعداد الاستضافة

### 1. استضافة cPanel:
```apache
# ملف: .htaccess
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L]

# إعدادات Passenger
PassengerEnabled On
PassengerAppRoot /home/username/public_html/shipping
PassengerStartupFile passenger_wsgi.py
PassengerAppType wsgi
PassengerPython /home/username/virtualenv/public_html/shipping/3.11/bin/python

# متغيرات البيئة
SetEnv DATABASE_URL "mysql+pymysql://username:password@localhost/database"
SetEnv SESSION_SECRET "your-secret-key-here"
SetEnv FLASK_ENV "production"
```

### 2. ملف WSGI:
```python
# ملف: passenger_wsgi.py
import sys
import os

# إضافة مسار التطبيق
sys.path.insert(0, os.path.dirname(__file__))

# إعداد متغيرات البيئة
os.environ.setdefault('FLASK_ENV', 'production')

# استيراد التطبيق
from app import app as application

if __name__ == "__main__":
    application.run()
```

### 3. المتطلبات:
```bash
# ملف: requirements.txt
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.0.0
PyMySQL==1.1.1
psycopg2-binary==2.9.9
Werkzeug==3.1.3
Jinja2==3.1.6
cryptography==3.4.8
email-validator==2.2.0
python-dateutil==2.9.0.post0
```

### 4. قاعدة البيانات:
```sql
-- MySQL Schema
CREATE DATABASE shipping_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shipping_system;

-- استيراد الهيكل
SOURCE database_schema.sql;

-- إضافة البيانات الأولية
SOURCE database_init.sql;
```

---

## 🔧 استكشاف الأخطاء

### 1. مشاكل قاعدة البيانات:
```python
# فحص الاتصال
try:
    db.create_all()
    print("✅ قاعدة البيانات متصلة")
except Exception as e:
    print(f"❌ خطأ في قاعدة البيانات: {e}")

# فحص الجداول
inspector = db.inspect(db.engine)
tables = inspector.get_table_names()
print(f"📊 الجداول الموجودة: {tables}")
```

### 2. مشاكل الاستضافة:
```python
# فحص Python
import sys
print(f"Python Version: {sys.version}")

# فحص المكتبات
try:
    import flask
    print(f"Flask Version: {flask.__version__}")
except ImportError as e:
    print(f"Flask غير مثبت: {e}")

# فحص المسارات
import os
print(f"Current Directory: {os.getcwd()}")
print(f"Python Path: {sys.path}")
```

### 3. فحص الأخطاء:
```python
# تسجيل الأخطاء
import logging
logging.basicConfig(level=logging.DEBUG)

# فحص ملفات السجل
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"خطأ داخلي: {error}")
    return render_template('error.html'), 500

@app.errorhandler(404)
def not_found(error):
    logging.warning(f"صفحة غير موجودة: {error}")
    return render_template('404.html'), 404
```

---

## 📊 إحصائيات النظام

### بيانات النظام الحالي:
- **16 جدول أساسي** في قاعدة البيانات
- **9 أنواع شحن** متاحة
- **18 نوع وثيقة** للمعاملات
- **160 نطاق تسعير** شامل
- **6 أنواع إجراءات** إدارية
- **مستخدم واحد افتراضي** (admin/admin123)

### الملفات والأحجام:
- **app.py**: 4,285 bytes - التطبيق الرئيسي
- **routes.py**: 160,198 bytes - معالجات الطلبات
- **models.py**: 30,727 bytes - نماذج قاعدة البيانات
- **translations.py**: 7,093 bytes - الترجمات
- **static/css/style.css**: تصميم شامل
- **templates/**: 24 قالب HTML

### المزايا المتقدمة:
- **دعم RTL**: كامل للنصوص العربية
- **تصميم متجاوب**: يعمل على جميع الأجهزة
- **نظام صلاحيات**: متعدد المستويات
- **تتبع مالي**: شامل للإيرادات والمصروفات
- **تصدير البيانات**: إلى CSV وPDF
- **طباعة الملصقات**: مع الباركود
- **البحث المتقدم**: في جميع الجداول
- **الإشعارات**: نظام تنبيهات شامل

---

## 🎓 الخلاصة والتوصيات

هذا النظام مصمم ليكون **حلاً شاملاً** لإدارة الشحن مع التركيز على:

1. **سهولة الاستخدام**: واجهة بسيطة باللغة العربية
2. **الموثوقية**: قاعدة بيانات محسنة ونظام أمان قوي
3. **القابلية للتوسع**: هيكل مرن يدعم الإضافات المستقبلية
4. **التوافق**: يعمل على جميع أنواع الاستضافة
5. **الأداء**: محسن للسرعة والكفاءة

### للمطورين الجدد:
- ابدأ بفهم `models.py` لمعرفة هيكل البيانات
- راجع `routes.py` لفهم تدفق العمليات
- استخدم `templates/base.html` كنقطة انطلاق للتصميم
- اتبع نمط الترجمة في `translations.py`

### للصيانة:
- راجع سجلات الأخطاء بانتظام
- حدّث أسعار المناطق حسب الحاجة
- أضف أنواع وثائق جديدة عند الطلب
- راقب الأداء وقم بالتحسينات المطلوبة

---

*تم إنشاء هذا الدليل بواسطة فريق التطوير - آخر تحديث: يوليو 2025*