<?php
/**
 * Shipments List
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

requireLogin();
requirePermission('shipments');

$shipmentModel = new Shipment();

// Handle filters
$filters = [
    'status' => sanitize($_GET['status'] ?? ''),
    'package_type' => sanitize($_GET['package_type'] ?? ''),
    'shipping_method' => sanitize($_GET['shipping_method'] ?? ''),
    'date_from' => sanitize($_GET['date_from'] ?? ''),
    'date_to' => sanitize($_GET['date_to'] ?? ''),
    'search' => sanitize($_GET['search'] ?? '')
];

// Handle search
if (!empty($filters['search'])) {
    $shipments = $shipmentModel->search($filters['search']);
} else {
    $shipments = $shipmentModel->getAll(1, 100, $filters);
}

// Handle delete request
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'delete') {
    if (verifyCSRFToken($_POST['csrf_token'] ?? '')) {
        $shipmentId = intval($_POST['shipment_id'] ?? 0);
        
        if ($shipmentModel->delete($shipmentId)) {
            logActivity('delete_shipment', "Deleted shipment ID: {$shipmentId}");
            setFlash('success', 'تم حذف الشحنة بنجاح');
        } else {
            setFlash('error', 'فشل في حذف الشحنة');
        }
        
        header('Location: shipments.php');
        exit;
    }
}

$pageTitle = __('shipments');
include 'views/header.php';
?>

<div class="container-fluid py-4">
    <!-- Filters -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-filter me-2"></i>فلترة الشحنات
                    </h6>
                </div>
                <div class="card-body">
                    <form method="GET" action="">
                        <div class="row">
                            <div class="col-md-3 mb-3">
                                <label for="search" class="form-label"><?= __('search') ?></label>
                                <input type="text" class="form-control" id="search" name="search" 
                                       value="<?= htmlspecialchars($filters['search']) ?>" 
                                       placeholder="رقم التتبع، اسم المرسل، اسم المستلم...">
                            </div>
                            
                            <div class="col-md-2 mb-3">
                                <label for="status" class="form-label">الحالة</label>
                                <select class="form-select" id="status" name="status">
                                    <option value="">جميع الحالات</option>
                                    <option value="created" <?= $filters['status'] === 'created' ? 'selected' : '' ?>>تم الإنشاء</option>
                                    <option value="packaged" <?= $filters['status'] === 'packaged' ? 'selected' : '' ?>>تم التعبئة</option>
                                    <option value="shipped" <?= $filters['status'] === 'shipped' ? 'selected' : '' ?>>تم الشحن</option>
                                    <option value="in_transit" <?= $filters['status'] === 'in_transit' ? 'selected' : '' ?>>في الطريق</option>
                                    <option value="delivered" <?= $filters['status'] === 'delivered' ? 'selected' : '' ?>>تم التسليم</option>
                                    <option value="cancelled" <?= $filters['status'] === 'cancelled' ? 'selected' : '' ?>>ملغي</option>
                                </select>
                            </div>
                            
                            <div class="col-md-2 mb-3">
                                <label for="package_type" class="form-label">نوع الطرد</label>
                                <select class="form-select" id="package_type" name="package_type">
                                    <option value="">جميع الأنواع</option>
                                    <option value="general" <?= $filters['package_type'] === 'general' ? 'selected' : '' ?>>عامة</option>
                                    <option value="document" <?= $filters['package_type'] === 'document' ? 'selected' : '' ?>>مستندات</option>
                                </select>
                            </div>
                            
                            <div class="col-md-2 mb-3">
                                <label for="shipping_method" class="form-label">طريقة الشحن</label>
                                <select class="form-select" id="shipping_method" name="shipping_method">
                                    <option value="">جميع الطرق</option>
                                    <option value="جوي" <?= $filters['shipping_method'] === 'جوي' ? 'selected' : '' ?>>جوي</option>
                                    <option value="بري" <?= $filters['shipping_method'] === 'بري' ? 'selected' : '' ?>>بري</option>
                                </select>
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <label class="form-label">نطاق التاريخ</label>
                                <div class="d-flex gap-2">
                                    <input type="date" class="form-control" name="date_from" value="<?= $filters['date_from'] ?>">
                                    <input type="date" class="form-control" name="date_to" value="<?= $filters['date_to'] ?>">
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-search me-2"></i><?= __('search') ?>
                            </button>
                            <a href="shipments.php" class="btn btn-secondary">
                                <i class="fas fa-times me-2"></i>مسح المرشحات
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Shipments Table -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h6 class="mb-0">
                        <i class="fas fa-box me-2"></i>
                        قائمة الشحنات (<?= count($shipments) ?> شحنة)
                    </h6>
                    <div class="d-flex gap-2">
                        <button onclick="printElement('shipmentsTable')" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-print me-2"></i>طباعة
                        </button>
                        <a href="add_shipment.php" class="btn btn-primary btn-sm">
                            <i class="fas fa-plus me-2"></i><?= __('add_shipment') ?>
                        </a>
                    </div>
                </div>
                <div class="card-body px-0 pt-0 pb-2">
                    <div class="table-responsive" id="shipmentsTable">
                        <table class="table align-items-center mb-0">
                            <thead>
                                <tr>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('tracking_number') ?></th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">الحالة</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"><?= __('sender_name') ?></th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"><?= __('receiver_name') ?></th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('weight') ?></th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">النوع</th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('price') ?></th>
                                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><?= __('created_at') ?></th>
                                    <th class="text-secondary opacity-7 no-print">الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php if (empty($shipments)): ?>
                                <tr>
                                    <td colspan="9" class="text-center py-4">
                                        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                                        <p class="text-muted"><?= __('no_data') ?></p>
                                    </td>
                                </tr>
                                <?php else: ?>
                                <?php foreach ($shipments as $shipment): ?>
                                <tr>
                                    <td>
                                        <div class="d-flex px-2 py-1">
                                            <div class="d-flex flex-column justify-content-center">
                                                <h6 class="mb-0 text-sm font-monospace">
                                                    <a href="tracking.php?number=<?= urlencode($shipment['tracking_number']) ?>" 
                                                       class="text-primary text-decoration-none">
                                                        <?= htmlspecialchars($shipment['tracking_number']) ?>
                                                    </a>
                                                </h6>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <?= getStatusBadge($shipment['status']) ?>
                                    </td>
                                    <td>
                                        <p class="text-xs text-secondary mb-0"><?= htmlspecialchars($shipment['sender_name']) ?></p>
                                        <?php if ($shipment['sender_phone']): ?>
                                        <p class="text-xs text-muted mb-0"><?= htmlspecialchars($shipment['sender_phone']) ?></p>
                                        <?php endif; ?>
                                    </td>
                                    <td>
                                        <p class="text-xs text-secondary mb-0"><?= htmlspecialchars($shipment['receiver_name']) ?></p>
                                        <?php if ($shipment['receiver_phone']): ?>
                                        <p class="text-xs text-muted mb-0"><?= htmlspecialchars($shipment['receiver_phone']) ?></p>
                                        <?php endif; ?>
                                    </td>
                                    <td class="align-middle text-center">
                                        <span class="text-secondary text-xs font-weight-bold">
                                            <?= $shipment['weight'] > 0 ? number_format($shipment['weight'], 3) . ' كغ' : '-' ?>
                                        </span>
                                    </td>
                                    <td class="align-middle text-center">
                                        <span class="badge bg-<?= $shipment['package_type'] === 'document' ? 'info' : 'primary' ?>">
                                            <?= $shipment['package_type'] === 'document' ? 'مستندات' : 'عامة' ?>
                                        </span>
                                        <?php if ($shipment['shipping_method']): ?>
                                        <br><?= getShippingMethodBadge($shipment['shipping_method']) ?>
                                        <?php endif; ?>
                                    </td>
                                    <td class="align-middle text-center">
                                        <span class="text-secondary text-xs font-weight-bold"><?= formatCurrency($shipment['price']) ?></span>
                                        <?php if ($shipment['remaining_amount'] > 0): ?>
                                        <br><small class="text-warning">متبقي: <?= formatCurrency($shipment['remaining_amount']) ?></small>
                                        <?php endif; ?>
                                    </td>
                                    <td class="align-middle text-center">
                                        <span class="text-secondary text-xs font-weight-bold"><?= formatDate($shipment['created_at']) ?></span>
                                    </td>
                                    <td class="align-middle no-print">
                                        <div class="d-flex gap-1">
                                            <a href="edit_shipment.php?id=<?= $shipment['id'] ?>" 
                                               class="btn btn-outline-primary btn-sm" title="تعديل">
                                                <i class="fas fa-edit"></i>
                                            </a>
                                            
                                            <a href="print_invoice.php?id=<?= $shipment['id'] ?>" 
                                               class="btn btn-outline-success btn-sm" title="طباعة فاتورة" target="_blank">
                                                <i class="fas fa-print"></i>
                                            </a>
                                            
                                            <button onclick="deleteShipment(<?= $shipment['id'] ?>)" 
                                                    class="btn btn-outline-danger btn-sm" title="حذف">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
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

<!-- Delete Modal -->
<div class="modal fade" id="deleteModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">تأكيد الحذف</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                هل أنت متأكد من حذف هذه الشحنة؟ لا يمكن التراجع عن هذا الإجراء.
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="shipment_id" id="deleteShipmentId">
                    <button type="submit" class="btn btn-danger">حذف</button>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
function deleteShipment(shipmentId) {
    document.getElementById('deleteShipmentId').value = shipmentId;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

// Initialize search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.closest('form').submit();
            }
        });
    }
});
</script>

<?php include 'views/footer.php'; ?>