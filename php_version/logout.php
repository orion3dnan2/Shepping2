<?php
/**
 * Logout
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

// Log activity if user is logged in
if (isLoggedIn()) {
    logActivity('logout', 'User logged out');
}

// Clear session data
session_destroy();
session_start();

// Redirect to login page
header('Location: login.php');
exit;
?>