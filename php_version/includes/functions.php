<?php
/**
 * Helper Functions
 * Shipping Management System - PHP Version
 */

/**
 * Generate unique tracking number
 */
function generateTrackingNumber() {
    $prefix = 'SHIP';
    $date = date('Ymd');
    $random = str_pad(rand(1, 999), 3, '0', STR_PAD_LEFT);
    return $prefix . '-' . $date . '-' . $random;
}

/**
 * Sanitize input data
 */
function sanitize($data) {
    if (is_array($data)) {
        return array_map('sanitize', $data);
    }
    return htmlspecialchars(trim($data), ENT_QUOTES, 'UTF-8');
}

/**
 * Validate email
 */
function isValidEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Validate phone number
 */
function isValidPhone($phone) {
    return preg_match('/^[\+]?[0-9\-\(\)\s]{8,20}$/', $phone);
}

/**
 * Format currency
 */
function formatCurrency($amount, $currency = 'د.ك') {
    return number_format($amount, 3) . ' ' . $currency;
}

/**
 * Format date for display
 */
function formatDate($date, $format = 'Y-m-d H:i') {
    if (empty($date) || $date === '0000-00-00 00:00:00') {
        return '';
    }
    return date($format, strtotime($date));
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
}

/**
 * Require login
 */
function requireLogin() {
    if (!isLoggedIn()) {
        header('Location: login.php');
        exit;
    }
}

/**
 * Check user permission
 */
function hasPermission($permission) {
    if (!isLoggedIn()) {
        return false;
    }
    
    $permissions = $_SESSION['permissions'] ?? [];
    return in_array($permission, $permissions) || $_SESSION['is_super_admin'] ?? false;
}

/**
 * Require permission
 */
function requirePermission($permission) {
    if (!hasPermission($permission)) {
        header('HTTP/1.0 403 Forbidden');
        include 'views/403.php';
        exit;
    }
}

/**
 * Flash message system
 */
function setFlash($type, $message) {
    $_SESSION['flash'][] = ['type' => $type, 'message' => $message];
}

function getFlash() {
    $flash = $_SESSION['flash'] ?? [];
    unset($_SESSION['flash']);
    return $flash;
}

/**
 * Redirect with message
 */
function redirect($url, $message = null, $type = 'success') {
    if ($message) {
        setFlash($type, $message);
    }
    header('Location: ' . $url);
    exit;
}

/**
 * Hash password
 */
function hashPassword($password) {
    return password_hash($password, PASSWORD_DEFAULT);
}

/**
 * Verify password
 */
function verifyPassword($password, $hash) {
    return password_verify($password, $hash);
}

/**
 * Generate CSRF token
 */
function generateCSRFToken() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verify CSRF token
 */
function verifyCSRFToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * Get status badge HTML
 */
function getStatusBadge($status) {
    $badges = [
        'created' => '<span class="badge bg-secondary">تم الإنشاء</span>',
        'packaged' => '<span class="badge bg-info">تم التعبئة</span>',
        'dispatching' => '<span class="badge bg-warning">جاري الإرسال</span>',
        'shipped' => '<span class="badge bg-primary">تم الشحن</span>',
        'in_transit' => '<span class="badge bg-info">في الطريق</span>',
        'received' => '<span class="badge bg-success">تم الاستلام</span>',
        'delivered' => '<span class="badge bg-success">تم التسليم</span>',
        'cancelled' => '<span class="badge bg-danger">ملغي</span>'
    ];
    
    return $badges[$status] ?? '<span class="badge bg-secondary">' . $status . '</span>';
}

/**
 * Get shipping method badge
 */
function getShippingMethodBadge($method) {
    $badges = [
        'جوي' => '<span class="badge bg-primary"><i class="fas fa-plane"></i> جوي</span>',
        'بري' => '<span class="badge bg-success"><i class="fas fa-truck"></i> بري</span>'
    ];
    
    return $badges[$method] ?? '<span class="badge bg-secondary">' . $method . '</span>';
}

/**
 * Calculate remaining amount
 */
function calculateRemainingAmount($price, $paidAmount) {
    return max(0, $price - $paidAmount);
}

/**
 * Log activity
 */
function logActivity($action, $details = '') {
    global $db;
    
    if (!isLoggedIn()) return;
    
    try {
        $db->insert('activity_log', [
            'user_id' => $_SESSION['user_id'],
            'action' => $action,
            'details' => $details,
            'ip_address' => $_SERVER['REMOTE_ADDR'] ?? '',
            'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? '',
            'created_at' => date('Y-m-d H:i:s')
        ]);
    } catch (Exception $e) {
        error_log("Activity log error: " . $e->getMessage());
    }
}

/**
 * Get user's full name
 */
function getUserName() {
    return $_SESSION['username'] ?? 'Guest';
}

/**
 * Include view with data
 */
function view($template, $data = []) {
    extract($data);
    include "views/{$template}.php";
}
?>