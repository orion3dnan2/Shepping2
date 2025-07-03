<?php
/**
 * Main Entry Point
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

// Check if user is logged in
if (!isLoggedIn()) {
    header('Location: login.php');
    exit;
}

// Get dashboard data
$shipmentModel = new Shipment();
$userModel = new User();

// Get statistics
$stats = $shipmentModel->getStatistics();
$recentShipments = $shipmentModel->getRecent(10);

// Dashboard data
$dashboardData = [
    'total_shipments' => $stats['total'] ?? 0,
    'pending_shipments' => $stats['status']['created'] ?? 0,
    'delivered_shipments' => $stats['status']['delivered'] ?? 0,
    'total_revenue' => $stats['revenue']['total_revenue'] ?? 0,
    'recent_shipments' => $recentShipments
];

$pageTitle = __('dashboard');
include 'views/header.php';
?>

<div class="container-fluid py-4">
    <!-- Statistics Cards -->
    <div class="row mb-4">
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
            <div class="card">
                <div class="card-body p-3">
                    <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-capitalize font-weight-bold"><?= __('total_shipments') ?></p>
                                <h5 class="font-weight-bolder mb-0"><?= number_format($dashboardData['total_shipments']) ?></h5>
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-primary shadow text-center border-radius-md">
                                <i class="fas fa-box text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
            <div class="card">
                <div class="card-body p-3">
                    <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-capitalize font-weight-bold"><?= __('pending_shipments') ?></p>
                                <h5 class="font-weight-bolder mb-0"><?= number_format($dashboardData['pending_shipments']) ?></h5>
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-warning shadow text-center border-radius-md">
                                <i class="fas fa-clock text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
            <div class="card">
                <div class="card-body p-3">
                    <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-capitalize font-weight-bold"><?= __('delivered_shipments') ?></p>
                                <h5 class="font-weight-bolder mb-0"><?= number_format($dashboardData['delivered_shipments']) ?></h5>
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-success shadow text-center border-radius-md">
                                <i class="fas fa-check text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-sm-6">
            <div class="card">
                <div class="card-body p-3">
                    <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-capitalize font-weight-bold"><?= __('total_revenue') ?></p>
                                <h5 class="font-weight-bolder mb-0"><?= formatCurrency($dashboardData['total_revenue']) ?></h5>
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-info shadow text-center border-radius-md">
                                <i class="fas fa-dollar-sign text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Quick Actions -->
    <div class="row mb-4">
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header pb-0">
                    <h6><?= __('add_shipment') ?></h6>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="add_shipment.php" class="btn btn-primary">
                            <i class="fas fa-plus me-2"></i><?= __('add_shipment') ?>
                        </a>
                        <a href="tracking.php" class="btn btn-info">
                            <i class="fas fa-search me-2"></i><?= __('tracking') ?>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header pb-0">
                    <h6>روابط سريعة</h6>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="shipments.php" class="btn btn-outline-primary">
                            <i class="fas fa-list me-2"></i><?= __('shipments') ?>
                        </a>
                        <a href="financial_center.php" class="btn btn-outline-success">
                            <i class="fas fa-chart-line me-2"></i><?= __('financial_center') ?>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Recent Shipments -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header pb-0">
                    <h6><?= __('recent_shipments') ?></h6>
                </div>
                <div class="card-body px-0 pt-0 pb-2">
                    <div class="table-responsive p-0">
                        <table class="table align-items-center mb-0">
                            <thead>
                                <tr>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('tracking_number') ?></th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"><?= __('sender_name') ?></th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"><?= __('receiver_name') ?></th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('status') ?></th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('price') ?></th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('created_at') ?></th>
                                    <th class="text-secondary opacity-7"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php if (empty($dashboardData['recent_shipments'])): ?>
                                <tr>
                                    <td colspan="7" class="text-center py-4">
                                        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                                        <p class="text-muted"><?= __('no_data') ?></p>
                                    </td>
                                </tr>
                                <?php else: ?>
                                <?php foreach ($dashboardData['recent_shipments'] as $shipment): ?>
                                <tr>
                                    <td>
                                        <div class="d-flex px-2 py-1">
                                            <div class="d-flex flex-column justify-content-center">
                                                <h6 class="mb-0 text-sm"><?= htmlspecialchars($shipment['tracking_number']) ?></h6>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <p class="text-xs text-secondary mb-0"><?= htmlspecialchars($shipment['sender_name']) ?></p>
                                    </td>
                                    <td>
                                        <p class="text-xs text-secondary mb-0"><?= htmlspecialchars($shipment['receiver_name']) ?></p>
                                    </td>
                                    <td class="align-middle text-center text-sm">
                                        <?= getStatusBadge($shipment['status']) ?>
                                    </td>
                                    <td class="align-middle text-center">
                                        <span class="text-secondary text-xs font-weight-bold"><?= formatCurrency($shipment['price']) ?></span>
                                    </td>
                                    <td class="align-middle text-center">
                                        <span class="text-secondary text-xs font-weight-bold"><?= formatDate($shipment['created_at']) ?></span>
                                    </td>
                                    <td class="align-middle">
                                        <a href="shipment.php?id=<?= $shipment['id'] ?>" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="View shipment">
                                            <?= __('edit') ?>
                                        </a>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                                <?php endif; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include 'views/footer.php'; ?>