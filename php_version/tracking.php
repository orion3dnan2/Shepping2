<?php
/**
 * Shipment Tracking
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

$shipmentModel = new Shipment();
$shipment = null;
$trackingNumber = sanitize($_GET['number'] ?? '');

// Handle tracking search
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['tracking_number'])) {
    $trackingNumber = sanitize($_POST['tracking_number']);
    header("Location: tracking.php?number=" . urlencode($trackingNumber));
    exit;
}

// Get shipment details if tracking number provided
if ($trackingNumber) {
    $shipment = $shipmentModel->getByTrackingNumber($trackingNumber);
}

$pageTitle = __('tracking');
include 'views/header.php';
?>

<div class="container-fluid py-4">
    <div class="row">
        <div class="col-12">
            <div class="card mb-4">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-search me-2"></i>تتبع الشحنة
                    </h6>
                </div>
                <div class="card-body">
                    <form method="POST" action="">
                        <div class="row align-items-end">
                            <div class="col-md-8">
                                <label for="tracking_number" class="form-label">رقم التتبع</label>
                                <input type="text" 
                                       class="form-control" 
                                       id="tracking_number" 
                                       name="tracking_number" 
                                       value="<?= htmlspecialchars($trackingNumber) ?>"
                                       placeholder="أدخل رقم التتبع..." 
                                       required>
                            </div>
                            <div class="col-md-4">
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="fas fa-search me-2"></i>تتبع
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <?php if ($trackingNumber && !$shipment): ?>
    <div class="row">
        <div class="col-12">
            <div class="alert alert-warning" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                لم يتم العثور على شحنة برقم التتبع: <strong><?= htmlspecialchars($trackingNumber) ?></strong>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <?php if ($shipment): ?>
    <div class="row">
        <div class="col-md-8">
            <!-- Shipment Timeline -->
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-route me-2"></i>مسار الشحنة
                    </h6>
                </div>
                <div class="card-body">
                    <div class="timeline">
                        <?php
                        $statuses = [
                            'created' => ['تم إنشاء الشحنة', 'fas fa-plus-circle', 'primary'],
                            'packaged' => ['تم تعبئة الشحنة', 'fas fa-box', 'info'],
                            'dispatching' => ['في الانتظار للشحن', 'fas fa-clock', 'warning'],
                            'shipped' => ['تم شحن الطرد', 'fas fa-truck', 'success'],
                            'in_transit' => ['في الطريق', 'fas fa-shipping-fast', 'primary'],
                            'received' => ['تم استلام الشحنة', 'fas fa-warehouse', 'info'],
                            'delivered' => ['تم التسليم', 'fas fa-check-circle', 'success'],
                            'cancelled' => ['تم إلغاء الشحنة', 'fas fa-times-circle', 'danger']
                        ];

                        $currentStatus = $shipment['status'];
                        $statusKeys = array_keys($statuses);
                        $currentIndex = array_search($currentStatus, $statusKeys);
                        
                        foreach ($statuses as $status => $info):
                            $statusIndex = array_search($status, $statusKeys);
                            $isActive = $statusIndex <= $currentIndex;
                            $isCurrent = $status === $currentStatus;
                            
                            // Skip cancelled if not the current status
                            if ($status === 'cancelled' && !$isCurrent) continue;
                        ?>
                        <div class="timeline-item <?= $isActive ? 'active' : '' ?> <?= $isCurrent ? 'current' : '' ?>">
                            <div class="timeline-icon bg-<?= $info[2] ?>">
                                <i class="<?= $info[1] ?>"></i>
                            </div>
                            <div class="timeline-content">
                                <h6 class="<?= $isActive ? 'text-' . $info[2] : 'text-muted' ?>"><?= $info[0] ?></h6>
                                <?php if ($isCurrent): ?>
                                <small class="text-muted">
                                    آخر تحديث: <?= formatDate($shipment['updated_at']) ?>
                                </small>
                                <?php endif; ?>
                            </div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <!-- Shipment Details -->
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-info-circle me-2"></i>تفاصيل الشحنة
                    </h6>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label text-muted">رقم التتبع</label>
                        <p class="mb-0 font-monospace"><?= htmlspecialchars($shipment['tracking_number']) ?></p>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label text-muted">الحالة الحالية</label>
                        <p class="mb-0"><?= getStatusBadge($shipment['status']) ?></p>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label text-muted">نوع الشحنة</label>
                        <p class="mb-0">
                            <span class="badge bg-<?= $shipment['package_type'] === 'document' ? 'info' : 'primary' ?>">
                                <?= $shipment['package_type'] === 'document' ? 'مستندات' : 'عامة' ?>
                            </span>
                        </p>
                    </div>
                    
                    <?php if ($shipment['shipping_method']): ?>
                    <div class="mb-3">
                        <label class="form-label text-muted">طريقة الشحن</label>
                        <p class="mb-0"><?= getShippingMethodBadge($shipment['shipping_method']) ?></p>
                    </div>
                    <?php endif; ?>
                    
                    <?php if ($shipment['weight'] > 0): ?>
                    <div class="mb-3">
                        <label class="form-label text-muted">الوزن</label>
                        <p class="mb-0"><?= number_format($shipment['weight'], 3) ?> كغ</p>
                    </div>
                    <?php endif; ?>
                    
                    <div class="mb-3">
                        <label class="form-label text-muted">السعر الإجمالي</label>
                        <p class="mb-0"><?= formatCurrency($shipment['price']) ?></p>
                    </div>
                    
                    <?php if ($shipment['remaining_amount'] > 0): ?>
                    <div class="mb-3">
                        <label class="form-label text-muted">المبلغ المتبقي</label>
                        <p class="mb-0 text-warning"><?= formatCurrency($shipment['remaining_amount']) ?></p>
                    </div>
                    <?php endif; ?>
                    
                    <div class="mb-3">
                        <label class="form-label text-muted">تاريخ الإنشاء</label>
                        <p class="mb-0"><?= formatDate($shipment['created_at']) ?></p>
                    </div>
                    
                    <?php if ($shipment['notes']): ?>
                    <div class="mb-3">
                        <label class="form-label text-muted">ملاحظات</label>
                        <p class="mb-0"><?= htmlspecialchars($shipment['notes']) ?></p>
                    </div>
                    <?php endif; ?>
                </div>
            </div>

            <!-- Contact Information -->
            <div class="card mt-4">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-address-book me-2"></i>معلومات الاتصال
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-6">
                            <h6 class="text-primary">المرسل</h6>
                            <p class="mb-1"><?= htmlspecialchars($shipment['sender_name']) ?></p>
                            <?php if ($shipment['sender_phone']): ?>
                            <p class="mb-0 text-muted small">
                                <i class="fas fa-phone me-1"></i>
                                <?= htmlspecialchars($shipment['sender_phone']) ?>
                            </p>
                            <?php endif; ?>
                        </div>
                        <div class="col-6">
                            <h6 class="text-success">المستلم</h6>
                            <p class="mb-1"><?= htmlspecialchars($shipment['receiver_name']) ?></p>
                            <?php if ($shipment['receiver_phone']): ?>
                            <p class="mb-0 text-muted small">
                                <i class="fas fa-phone me-1"></i>
                                <?= htmlspecialchars($shipment['receiver_phone']) ?>
                            </p>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php endif; ?>
</div>

<style>
.timeline {
    position: relative;
    padding: 20px 0;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 25px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #e9ecef;
}

.timeline-item {
    position: relative;
    padding-left: 60px;
    margin-bottom: 30px;
}

.timeline-item.active .timeline-icon {
    background: var(--bs-primary) !important;
}

.timeline-item.current .timeline-icon {
    animation: pulse 2s infinite;
}

.timeline-icon {
    position: absolute;
    left: 15px;
    top: 0;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #e9ecef;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    z-index: 1;
}

.timeline-content {
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

@media (max-width: 768px) {
    .timeline::before {
        left: 15px;
    }
    
    .timeline-item {
        padding-left: 40px;
    }
    
    .timeline-icon {
        left: 5px;
    }
}
</style>

<?php include 'views/footer.php'; ?>