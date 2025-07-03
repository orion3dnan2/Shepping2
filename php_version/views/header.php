<!DOCTYPE html>
<html lang="<?= getCurrentLanguage() ?>" dir="<?= isRTL() ? 'rtl' : 'ltr' ?>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $pageTitle ?? 'Dashboard' ?> - <?= APP_NAME ?></title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Tajawal', Arial, sans-serif;
            background-color: #f8f9fa;
        }
        
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: 700;
            font-size: 1.25rem;
        }
        
        .sidebar {
            background: #fff;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            min-height: calc(100vh - 56px);
            padding-top: 1rem;
        }
        
        .sidebar .nav-link {
            color: #495057;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            margin: 0.25rem 1rem;
            transition: all 0.3s;
        }
        
        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .sidebar .nav-link i {
            width: 20px;
        }
        
        .main-content {
            background-color: #f8f9fa;
            min-height: calc(100vh - 56px);
        }
        
        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-2px);
        }
        
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px 12px 0 0 !important;
            font-weight: 600;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 8px;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        }
        
        .table {
            border-radius: 8px;
            overflow: hidden;
        }
        
        .table thead th {
            background: #f8f9fa;
            border: none;
            font-weight: 600;
            color: #495057;
        }
        
        .badge {
            font-size: 0.75rem;
            padding: 0.5em 0.75em;
            border-radius: 6px;
        }
        
        .alert {
            border: none;
            border-radius: 8px;
        }
        
        /* RTL Adjustments */
        [dir="rtl"] .sidebar {
            box-shadow: -2px 0 10px rgba(0,0,0,0.1);
        }
        
        [dir="rtl"] .sidebar .nav-link {
            text-align: right;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            
            .sidebar.show {
                display: block;
                position: fixed;
                top: 56px;
                left: 0;
                width: 100%;
                z-index: 1000;
                background: white;
            }
            
            .main-content {
                margin-left: 0 !important;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <button class="navbar-toggler d-lg-none" type="button" data-bs-toggle="collapse" data-bs-target="#sidebar">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <a class="navbar-brand" href="index.php">
                <i class="fas fa-shipping-fast me-2"></i>
                <?= APP_NAME ?>
            </a>
            
            <div class="navbar-nav ms-auto">
                <!-- Language Toggle -->
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-language me-1"></i>
                        <?= getCurrentLanguage() === 'ar' ? 'العربية' : 'English' ?>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="?lang=ar">العربية</a></li>
                        <li><a class="dropdown-item" href="?lang=en">English</a></li>
                    </ul>
                </div>
                
                <!-- User Menu -->
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user me-1"></i>
                        <?= getUserName() ?>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="profile.php"><i class="fas fa-user me-2"></i><?= __('profile') ?></a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="logout.php"><i class="fas fa-sign-out-alt me-2"></i><?= __('logout') ?></a></li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>

    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-3 col-lg-2 d-md-block sidebar collapse" id="sidebar">
                <div class="position-sticky">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link <?= basename($_SERVER['PHP_SELF']) === 'index.php' ? 'active' : '' ?>" href="index.php">
                                <i class="fas fa-tachometer-alt me-2"></i>
                                <?= __('dashboard') ?>
                            </a>
                        </li>
                        
                        <?php if (hasPermission('add_shipment')): ?>
                        <li class="nav-item">
                            <a class="nav-link <?= basename($_SERVER['PHP_SELF']) === 'add_shipment.php' ? 'active' : '' ?>" href="add_shipment.php">
                                <i class="fas fa-plus me-2"></i>
                                <?= __('add_shipment') ?>
                            </a>
                        </li>
                        <?php endif; ?>
                        
                        <?php if (hasPermission('shipments')): ?>
                        <li class="nav-item">
                            <a class="nav-link <?= basename($_SERVER['PHP_SELF']) === 'shipments.php' ? 'active' : '' ?>" href="shipments.php">
                                <i class="fas fa-box me-2"></i>
                                <?= __('shipments') ?>
                            </a>
                        </li>
                        <?php endif; ?>
                        
                        <?php if (hasPermission('tracking')): ?>
                        <li class="nav-item">
                            <a class="nav-link <?= basename($_SERVER['PHP_SELF']) === 'tracking.php' ? 'active' : '' ?>" href="tracking.php">
                                <i class="fas fa-search me-2"></i>
                                <?= __('tracking') ?>
                            </a>
                        </li>
                        <?php endif; ?>
                        
                        <?php if (hasPermission('expenses')): ?>
                        <li class="nav-item">
                            <a class="nav-link <?= basename($_SERVER['PHP_SELF']) === 'financial_center.php' ? 'active' : '' ?>" href="financial_center.php">
                                <i class="fas fa-chart-line me-2"></i>
                                <?= __('financial_center') ?>
                            </a>
                        </li>
                        <?php endif; ?>
                        
                        <?php if (hasPermission('settings')): ?>
                        <li class="nav-item">
                            <a class="nav-link <?= basename($_SERVER['PHP_SELF']) === 'settings.php' ? 'active' : '' ?>" href="settings.php">
                                <i class="fas fa-cog me-2"></i>
                                <?= __('settings') ?>
                            </a>
                        </li>
                        <?php endif; ?>
                    </ul>
                </div>
            </nav>

            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 main-content">
                <?php
                // Display flash messages
                $flashMessages = getFlash();
                foreach ($flashMessages as $message):
                ?>
                <div class="alert alert-<?= $message['type'] === 'error' ? 'danger' : $message['type'] ?> alert-dismissible fade show mt-3">
                    <?= htmlspecialchars($message['message']) ?>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                <?php endforeach; ?>
                
                <?php
                // Handle language change
                if (isset($_GET['lang'])) {
                    setLanguage($_GET['lang']);
                    header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
                    exit;
                }
                ?>