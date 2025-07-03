<?php
/**
 * Configuration Settings
 * Shipping Management System - PHP Version
 */

// Error reporting for development
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Session configuration
session_start();

// Set timezone
date_default_timezone_set('Asia/Kuwait');

// App configuration
define('APP_NAME', 'مرسال إكسبرس للاستيراد والتصدير');
define('APP_VERSION', '2.0.0');
define('BASE_URL', '/shipping/');

// Database configuration
define('DB_HOST', $_ENV['DB_HOST'] ?? 'localhost');
define('DB_NAME', $_ENV['DB_NAME'] ?? 'shipping_system');
define('DB_USER', $_ENV['DB_USER'] ?? 'root');
define('DB_PASS', $_ENV['DB_PASS'] ?? '');

// Security
define('SECRET_KEY', $_ENV['SECRET_KEY'] ?? 'your-secret-key-change-in-production');

// Upload settings
define('MAX_UPLOAD_SIZE', 16777216); // 16MB
define('UPLOAD_PATH', __DIR__ . '/../uploads/');

// Language settings
define('DEFAULT_LANGUAGE', 'ar');
$_SESSION['language'] = $_SESSION['language'] ?? DEFAULT_LANGUAGE;

// Auto-load classes
spl_autoload_register(function($className) {
    $paths = [
        __DIR__ . '/../models/',
        __DIR__ . '/../controllers/',
        __DIR__ . '/../includes/'
    ];
    
    foreach ($paths as $path) {
        $file = $path . $className . '.php';
        if (file_exists($file)) {
            require_once $file;
            return;
        }
    }
});

// Include helper functions
require_once __DIR__ . '/../includes/functions.php';
require_once __DIR__ . '/../includes/translations.php';

// Initialize database
try {
    $db = new Database();
} catch (Exception $e) {
    die("Database connection error: " . $e->getMessage());
}
?>