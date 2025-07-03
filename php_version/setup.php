<?php
/**
 * Database Setup Script
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

// Only allow setup if no admin users exist
$userModel = new User();
$existingAdmins = $userModel->getAll();

if (!empty($existingAdmins)) {
    die('Setup already completed. Admin users already exist.');
}

$message = '';
$error = '';

// Handle setup form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        // Create database tables
        createDatabaseTables();
        
        // Create default admin user
        $adminData = [
            'username' => 'admin',
            'email' => 'admin@shipping.com',
            'password' => 'admin123',
            'is_super_admin' => true,
            'permissions' => ['home', 'shipments', 'tracking', 'reports', 'expenses', 'add_shipment', 'settings']
        ];
        
        $userModel->create($adminData);
        
        // Create sample data
        createSampleData();
        
        $message = 'تم إعداد النظام بنجاح! يمكنك الآن تسجيل الدخول باستخدام: admin / admin123';
        
    } catch (Exception $e) {
        $error = 'خطأ في الإعداد: ' . $e->getMessage();
    }
}

function createDatabaseTables() {
    global $db;
    
    // Admin table
    $db->query("
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(64) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password_hash VARCHAR(256) NOT NULL,
            is_super_admin BOOLEAN DEFAULT FALSE,
            permissions JSON,
            last_login DATETIME NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
    
    // Shipment table
    $db->query("
        CREATE TABLE IF NOT EXISTS shipment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tracking_number VARCHAR(50) NOT NULL UNIQUE,
            sender_name VARCHAR(100) NOT NULL,
            sender_phone VARCHAR(20),
            sender_address TEXT,
            receiver_name VARCHAR(100) NOT NULL,
            receiver_phone VARCHAR(20),
            receiver_address TEXT,
            weight DECIMAL(10,3) DEFAULT 0,
            price DECIMAL(10,3) DEFAULT 0,
            paid_amount DECIMAL(10,3) DEFAULT 0,
            remaining_amount DECIMAL(10,3) DEFAULT 0,
            package_contents TEXT,
            package_type VARCHAR(50) DEFAULT 'general',
            shipping_method VARCHAR(20),
            zone VARCHAR(50),
            has_packaging BOOLEAN DEFAULT FALSE,
            waybill_price DECIMAL(10,3) DEFAULT 0,
            status VARCHAR(50) DEFAULT 'created',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
    
    // Shipment types table
    $db->query("
        CREATE TABLE IF NOT EXISTS shipment_type (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name_ar VARCHAR(100) NOT NULL,
            name_en VARCHAR(100) NOT NULL,
            price_per_kg DECIMAL(10,3) DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
    
    // Document types table
    $db->query("
        CREATE TABLE IF NOT EXISTS document_type (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name_ar VARCHAR(100) NOT NULL,
            name_en VARCHAR(100) NOT NULL,
            price DECIMAL(10,3) DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
    
    // Financial transactions table
    $db->query("
        CREATE TABLE IF NOT EXISTS financial_transaction (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_type VARCHAR(20) NOT NULL,
            revenue_type VARCHAR(50),
            shipping_type VARCHAR(50),
            name VARCHAR(200) NOT NULL,
            amount DECIMAL(10,3) NOT NULL,
            category VARCHAR(100),
            description TEXT,
            transaction_date DATE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
    
    // Activity log table
    $db->query("
        CREATE TABLE IF NOT EXISTS activity_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action VARCHAR(100) NOT NULL,
            details TEXT,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES admin(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
    
    // Global settings table
    $db->query("
        CREATE TABLE IF NOT EXISTS global_settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            setting_name VARCHAR(100) NOT NULL UNIQUE,
            setting_value DECIMAL(10,3) DEFAULT 0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ");
}

function createSampleData() {
    global $db;
    
    // Sample shipment types
    $shipmentTypes = [
        ['إلكترونيات', 'Electronics', 5.000],
        ['ملابس', 'Clothes', 3.000],
        ['كتب', 'Books', 2.000],
        ['أدوية', 'Medicine', 8.000],
        ['طعام', 'Food', 4.000],
        ['عامة', 'General', 3.500]
    ];
    
    foreach ($shipmentTypes as $type) {
        $db->query("
            INSERT IGNORE INTO shipment_type (name_ar, name_en, price_per_kg) 
            VALUES (?, ?, ?)
        ", $type);
    }
    
    // Sample document types
    $documentTypes = [
        ['الشهادات الرسمية', 'Official Certificates', 25.000],
        ['الأوراق العامة', 'General Documents', 15.000],
        ['التوثيقات القانونية', 'Legal Documents', 35.000],
        ['الأوراق الطبية', 'Medical Documents', 20.000],
        ['أوراق التعليم', 'Educational Documents', 30.000]
    ];
    
    foreach ($documentTypes as $type) {
        $db->query("
            INSERT IGNORE INTO document_type (name_ar, name_en, price) 
            VALUES (?, ?, ?)
        ", $type);
    }
    
    // Global settings
    $settings = [
        ['packaging_price', 2.500],
        ['waybill_price', 1.500],
        ['price_per_kg', 4.000]
    ];
    
    foreach ($settings as $setting) {
        $db->query("
            INSERT IGNORE INTO global_settings (setting_name, setting_value) 
            VALUES (?, ?)
        ", $setting);
    }
}
?>

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إعداد النظام - <?= APP_NAME ?></title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Tajawal', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .setup-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            max-width: 500px;
            width: 100%;
        }
        
        .setup-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        .setup-body {
            padding: 2rem;
        }
        
        .btn-setup {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: 600;
        }
        
        .logo {
            width: 80px;
            height: 80px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
        }
        
        .logo i {
            color: #667eea;
            font-size: 32px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="setup-card">
                    <div class="setup-header">
                        <div class="logo">
                            <i class="fas fa-cogs"></i>
                        </div>
                        <h3 class="mb-0">إعداد النظام</h3>
                        <p class="mb-0 opacity-75"><?= APP_NAME ?></p>
                    </div>
                    
                    <div class="setup-body">
                        <?php if ($message): ?>
                        <div class="alert alert-success" role="alert">
                            <i class="fas fa-check-circle me-2"></i>
                            <?= htmlspecialchars($message) ?>
                            <div class="mt-3">
                                <a href="login.php" class="btn btn-success">
                                    <i class="fas fa-sign-in-alt me-2"></i>تسجيل الدخول
                                </a>
                            </div>
                        </div>
                        <?php elseif ($error): ?>
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            <?= htmlspecialchars($error) ?>
                        </div>
                        <?php else: ?>
                        <div class="text-center mb-4">
                            <h5>مرحباً بك في نظام إدارة الشحن</h5>
                            <p class="text-muted">انقر على الزر أدناه لإعداد النظام وإنشاء المستخدم الإداري الأول</p>
                        </div>
                        
                        <div class="list-group mb-4">
                            <div class="list-group-item">
                                <i class="fas fa-database text-primary me-2"></i>
                                إنشاء جداول قاعدة البيانات
                            </div>
                            <div class="list-group-item">
                                <i class="fas fa-user-shield text-success me-2"></i>
                                إنشاء المستخدم الإداري الأول
                            </div>
                            <div class="list-group-item">
                                <i class="fas fa-box text-info me-2"></i>
                                إضافة بيانات نموذجية
                            </div>
                            <div class="list-group-item">
                                <i class="fas fa-cog text-warning me-2"></i>
                                تكوين الإعدادات الأساسية
                            </div>
                        </div>
                        
                        <form method="POST" action="">
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-setup">
                                    <i class="fas fa-play me-2"></i>بدء الإعداد
                                </button>
                            </div>
                        </form>
                        <?php endif; ?>
                        
                        <div class="text-center mt-4">
                            <small class="text-muted">
                                النظام سيقوم بإنشاء المستخدم: <strong>admin</strong><br>
                                كلمة المرور: <strong>admin123</strong>
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>