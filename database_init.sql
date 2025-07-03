-- إعادة إنشاء قاعدة البيانات للنظام
-- نظام إدارة الشحن - قاعدة بيانات PostgreSQL محسنة

-- إضافة المشرف الافتراضي
INSERT INTO admin (username, password_hash, permissions, is_super_admin, created_at) 
VALUES ('admin', 'scrypt:32768:8:1$iJVhYEOY5LtWnxs2$ec2eabbffc41e54c25da8478de496560ce90c8084ffc7a5d6a684dfee49c79cc67eea2d131757de2505f7b7965c515a1c8dd60d905ff811d49363d9be0deaee1', 
        '{"shipments": true, "financial_center": true, "settings": true}', 
        true, NOW())
ON CONFLICT (username) DO UPDATE SET 
    password_hash = EXCLUDED.password_hash,
    permissions = EXCLUDED.permissions,
    is_super_admin = EXCLUDED.is_super_admin;

-- إضافة أنواع الشحن الأساسية
INSERT INTO shipment_type (name_ar, name_en, price, is_active, created_at) VALUES
('شحن عام', 'General Shipping', 0.0, true, NOW()),
('وثائق', 'Documents', 0.0, true, NOW()),
('طرود', 'Packages', 0.0, true, NOW()),
('بضائع تجارية', 'Commercial Goods', 0.0, true, NOW()),
('إلكترونيات', 'Electronics', 0.0, true, NOW()),
('طعام ومشروبات', 'Food & Beverages', 0.0, true, NOW()),
('ملابس', 'Clothing', 0.0, true, NOW()),
('أدوية', 'Medicines', 0.0, true, NOW()),
('كتب', 'Books', 0.0, true, NOW())
ON CONFLICT (name_ar) DO NOTHING;

-- إضافة أنواع الوثائق
INSERT INTO document_type (name_ar, name_en, price, is_active, created_at) VALUES
('توثيق خارجية', 'Foreign Affairs Authentication', 50.0, true, NOW()),
('توثيق تعليم عالي', 'Higher Education Authentication', 30.0, true, NOW()),
('أدلة جنائية', 'Criminal Record', 25.0, true, NOW()),
('شهادة ثانوية', 'Secondary Certificate', 40.0, true, NOW()),
('شهادة جامعية', 'University Certificate', 60.0, true, NOW()),
('قسيمة زواج مدرجة', 'Registered Marriage Certificate', 35.0, true, NOW()),
('قسيمة زواج غير مدرجة', 'Unregistered Marriage Certificate', 45.0, true, NOW()),
('شهادة جامعية تفاصيل', 'University Certificate Details', 70.0, true, NOW()),
('شهادة ميلاد', 'Birth Certificate', 20.0, true, NOW()),
('شهادة وفاة', 'Death Certificate', 20.0, true, NOW()),
('جواز سفر', 'Passport', 80.0, true, NOW()),
('رخصة قيادة', 'Driving License', 30.0, true, NOW()),
('شهادة عسكرية', 'Military Certificate', 40.0, true, NOW())
ON CONFLICT (name_ar) DO NOTHING;

-- إضافة أنواع الإجراءات
INSERT INTO procedure_type (name_ar, name_en, price, is_active, created_at) VALUES
('استخراج شهادة ثانوية', 'Secondary Certificate Extraction', 40.0, true, NOW()),
('استخراج شهادة جامعية', 'University Certificate Extraction', 60.0, true, NOW()),
('استخراج قسيمة زواج', 'Marriage Certificate Extraction', 35.0, true, NOW()),
('استخراج شهادة ميلاد', 'Birth Certificate Extraction', 20.0, true, NOW()),
('استخراج شهادة وفاة', 'Death Certificate Extraction', 20.0, true, NOW()),
('تجديد جواز سفر', 'Passport Renewal', 100.0, true, NOW())
ON CONFLICT (name_ar) DO NOTHING;

-- إضافة نطاقات التسعير للاتجاهين
INSERT INTO zone_pricing (zone_name_ar, zone_name_en, price_per_kg, direction, is_active, created_at) VALUES
-- من الكويت للسودان
('الخرطوم', 'Khartoum', 5.0, 'kuwait_to_sudan', true, NOW()),
('أم درمان', 'Omdurman', 5.0, 'kuwait_to_sudan', true, NOW()),
('بحري', 'Bahri', 5.0, 'kuwait_to_sudan', true, NOW()),
('مدني', 'Madani', 5.5, 'kuwait_to_sudan', true, NOW()),
('كسلا', 'Kassala', 6.0, 'kuwait_to_sudan', true, NOW()),
('بورتسودان', 'Port Sudan', 6.5, 'kuwait_to_sudan', true, NOW()),
('الجزيرة', 'Gezira', 5.5, 'kuwait_to_sudan', true, NOW()),
('سنار', 'Sennar', 6.0, 'kuwait_to_sudan', true, NOW()),
('النيل الأزرق', 'Blue Nile', 6.5, 'kuwait_to_sudan', true, NOW()),
('النيل الأبيض', 'White Nile', 6.0, 'kuwait_to_sudan', true, NOW()),
('كردفان', 'Kordofan', 7.0, 'kuwait_to_sudan', true, NOW()),
('دارفور', 'Darfur', 8.0, 'kuwait_to_sudan', true, NOW()),
('جنوب كردفان', 'South Kordofan', 7.5, 'kuwait_to_sudan', true, NOW()),
('القضارف', 'Gedaref', 6.0, 'kuwait_to_sudan', true, NOW()),
('الشمالية', 'Northern', 6.5, 'kuwait_to_sudan', true, NOW()),
('نهر النيل', 'River Nile', 6.0, 'kuwait_to_sudan', true, NOW()),
('البحر الأحمر', 'Red Sea', 7.0, 'kuwait_to_sudan', true, NOW()),
('كسلا', 'Kassala State', 6.0, 'kuwait_to_sudan', true, NOW()),
('المناطق النائية', 'Remote Areas', 9.0, 'kuwait_to_sudan', true, NOW()),

-- من السودان للكويت
('الخرطوم', 'Khartoum', 5.5, 'sudan_to_kuwait', true, NOW()),
('أم درمان', 'Omdurman', 5.5, 'sudan_to_kuwait', true, NOW()),
('بحري', 'Bahri', 5.5, 'sudan_to_kuwait', true, NOW()),
('مدني', 'Madani', 6.0, 'sudan_to_kuwait', true, NOW()),
('كسلا', 'Kassala', 6.5, 'sudan_to_kuwait', true, NOW()),
('بورتسودان', 'Port Sudan', 7.0, 'sudan_to_kuwait', true, NOW()),
('الجزيرة', 'Gezira', 6.0, 'sudan_to_kuwait', true, NOW()),
('سنار', 'Sennar', 6.5, 'sudan_to_kuwait', true, NOW()),
('النيل الأزرق', 'Blue Nile', 7.0, 'sudan_to_kuwait', true, NOW()),
('النيل الأبيض', 'White Nile', 6.5, 'sudan_to_kuwait', true, NOW()),
('كردفان', 'Kordofan', 7.5, 'sudan_to_kuwait', true, NOW()),
('دارفور', 'Darfur', 8.5, 'sudan_to_kuwait', true, NOW()),
('جنوب كردفان', 'South Kordofan', 8.0, 'sudan_to_kuwait', true, NOW()),
('القضارف', 'Gedaref', 6.5, 'sudan_to_kuwait', true, NOW()),
('الشمالية', 'Northern', 7.0, 'sudan_to_kuwait', true, NOW()),
('نهر النيل', 'River Nile', 6.5, 'sudan_to_kuwait', true, NOW()),
('البحر الأحمر', 'Red Sea', 7.5, 'sudan_to_kuwait', true, NOW()),
('كسلا', 'Kassala State', 6.5, 'sudan_to_kuwait', true, NOW()),
('المناطق النائية', 'Remote Areas', 9.5, 'sudan_to_kuwait', true, NOW())
ON CONFLICT (zone_name_ar, direction) DO NOTHING;

-- إضافة أنواع التغليف
INSERT INTO packaging_type (name_ar, name_en, cost, is_active, created_at) VALUES
('صندوق صغير', 'Small Box', 2.0, true, NOW()),
('صندوق متوسط', 'Medium Box', 3.0, true, NOW()),
('صندوق كبير', 'Large Box', 5.0, true, NOW()),
('ظرف', 'Envelope', 1.0, true, NOW()),
('بدون تغليف', 'No Packaging', 0.0, true, NOW())
ON CONFLICT (name_ar) DO NOTHING;

-- إضافة الإعدادات العامة
INSERT INTO global_settings (setting_key, setting_value, created_at, updated_at) VALUES
('packaging_price', 2.000, NOW(), NOW()),
('policy_price', 5.000, NOW(), NOW()),
('comment_price', 1.000, NOW(), NOW()),
('default_zone', 1.000, NOW(), NOW()),
('currency_symbol', 0.000, NOW(), NOW())
ON CONFLICT (setting_key) DO UPDATE SET 
    setting_value = EXCLUDED.setting_value,
    updated_at = NOW();

-- إضافة تكاليف الشحن الجوي
INSERT INTO air_shipping_costs (price_per_kg, packaging_price, kuwait_transport_price, sudan_transport_price, clearance_price, created_at, updated_at) VALUES
(8.0, 2.0, 3.0, 4.0, 5.0, NOW(), NOW())
ON CONFLICT DO NOTHING;

-- إضافة تكاليف الوثائق
INSERT INTO document_costs (doc_authentication_foreign, doc_authentication_education, doc_criminal_record, doc_secondary_certificate, doc_university_certificate, doc_marriage_registered, doc_marriage_unregistered, doc_university_details, created_at, updated_at) VALUES
(50.0, 30.0, 25.0, 40.0, 60.0, 35.0, 45.0, 70.0, NOW(), NOW())
ON CONFLICT DO NOTHING;

-- إضافة إشعار ترحيب
INSERT INTO notification (title, message, tracking_number, shipment_type, is_read, created_at) VALUES
('مرحباً بك في نظام إدارة الشحن', 'تم تهيئة النظام بنجاح. يمكنك الآن البدء في إدارة الشحنات والمعاملات المالية.', NULL, NULL, false, NOW())
ON CONFLICT DO NOTHING;