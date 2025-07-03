<?php
/**
 * Edit Shipment
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

requireLogin();
requirePermission('shipments');

$shipmentModel = new Shipment();
$shipmentId = intval($_GET['id'] ?? 0);

// Get shipment details
$shipment = $shipmentModel->getById($shipmentId);
if (!$shipment) {
    setFlash('error', 'الشحنة غير موجودة');
    header('Location: shipments.php');
    exit;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (verifyCSRFToken($_POST['csrf_token'] ?? '')) {
        try {
            $data = [
                'sender_name' => sanitize($_POST['sender_name'] ?? ''),
                'sender_phone' => sanitize($_POST['sender_phone'] ?? ''),
                'sender_address' => sanitize($_POST['sender_address'] ?? ''),
                'receiver_name' => sanitize($_POST['receiver_name'] ?? ''),
                'receiver_phone' => sanitize($_POST['receiver_phone'] ?? ''),
                'receiver_address' => sanitize($_POST['receiver_address'] ?? ''),
                'weight' => floatval($_POST['weight'] ?? 0),
                'price' => floatval($_POST['price'] ?? 0),
                'paid_amount' => floatval($_POST['paid_amount'] ?? 0),
                'package_contents' => sanitize($_POST['package_contents'] ?? ''),
                'package_type' => sanitize($_POST['package_type'] ?? 'general'),
                'shipping_method' => sanitize($_POST['shipping_method'] ?? ''),
                'zone' => sanitize($_POST['zone'] ?? ''),
                'has_packaging' => isset($_POST['has_packaging']),
                'waybill_price' => floatval($_POST['waybill_price'] ?? 0),
                'status' => sanitize($_POST['status'] ?? $shipment['status']),
                'notes' => sanitize($_POST['notes'] ?? '')
            ];

            // Calculate remaining amount
            $data['remaining_amount'] = $data['price'] - $data['paid_amount'];
            
            if ($shipmentModel->update($shipmentId, $data)) {
                logActivity('edit_shipment', "Updated shipment: {$shipment['tracking_number']}");
                setFlash('success', 'تم تحديث الشحنة بنجاح');
                header('Location: shipments.php');
                exit;
            } else {
                setFlash('error', 'فشل في تحديث الشحنة');
            }
        } catch (Exception $e) {
            setFlash('error', 'خطأ: ' . $e->getMessage());
        }
    } else {
        setFlash('error', 'رمز الحماية غير صحيح');
    }
}

$pageTitle = 'تعديل الشحنة';
include 'views/header.php';
?>

<div class="container-fluid py-4">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">
                            <i class="fas fa-edit me-2"></i>تعديل الشحنة - <?= htmlspecialchars($shipment['tracking_number']) ?>
                        </h6>
                        <a href="shipments.php" class="btn btn-outline-secondary btn-sm">
                            <i class="fas fa-arrow-right me-2"></i>العودة
                        </a>
                    </div>
                </div>
                <div class="card-body">
                    <form method="POST" action="">
                        <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                        
                        <div class="row">
                            <!-- Sender Information -->
                            <div class="col-md-6">
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h6 class="mb-0">
                                            <i class="fas fa-user text-primary me-2"></i>معلومات المرسل
                                        </h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <label for="sender_name" class="form-label">اسم المرسل</label>
                                            <input type="text" 
                                                   class="form-control" 
                                                   id="sender_name" 
                                                   name="sender_name" 
                                                   value="<?= htmlspecialchars($shipment['sender_name']) ?>"
                                                   required>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label for="sender_phone" class="form-label">رقم الهاتف</label>
                                            <input type="tel" 
                                                   class="form-control" 
                                                   id="sender_phone" 
                                                   name="sender_phone" 
                                                   value="<?= htmlspecialchars($shipment['sender_phone']) ?>">
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label for="sender_address" class="form-label">العنوان</label>
                                            <textarea class="form-control" 
                                                      id="sender_address" 
                                                      name="sender_address" 
                                                      rows="3"><?= htmlspecialchars($shipment['sender_address']) ?></textarea>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Receiver Information -->
                            <div class="col-md-6">
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h6 class="mb-0">
                                            <i class="fas fa-user-check text-success me-2"></i>معلومات المستلم
                                        </h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <label for="receiver_name" class="form-label">اسم المستلم</label>
                                            <input type="text" 
                                                   class="form-control" 
                                                   id="receiver_name" 
                                                   name="receiver_name" 
                                                   value="<?= htmlspecialchars($shipment['receiver_name']) ?>"
                                                   required>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label for="receiver_phone" class="form-label">رقم الهاتف</label>
                                            <input type="tel" 
                                                   class="form-control" 
                                                   id="receiver_phone" 
                                                   name="receiver_phone" 
                                                   value="<?= htmlspecialchars($shipment['receiver_phone']) ?>">
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label for="receiver_address" class="form-label">العنوان</label>
                                            <textarea class="form-control" 
                                                      id="receiver_address" 
                                                      name="receiver_address" 
                                                      rows="3"><?= htmlspecialchars($shipment['receiver_address']) ?></textarea>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Shipment Details -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h6 class="mb-0">
                                    <i class="fas fa-box text-info me-2"></i>تفاصيل الشحنة
                                </h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-3">
                                        <div class="mb-3">
                                            <label for="package_type" class="form-label">نوع الطرد</label>
                                            <select class="form-select" id="package_type" name="package_type" onchange="toggleFields()">
                                                <option value="general" <?= $shipment['package_type'] === 'general' ? 'selected' : '' ?>>عامة</option>
                                                <option value="document" <?= $shipment['package_type'] === 'document' ? 'selected' : '' ?>>مستندات</option>
                                            </select>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-3" id="shipping_method_field" style="display: <?= $shipment['package_type'] === 'document' ? 'none' : 'block' ?>;">
                                        <div class="mb-3">
                                            <label for="shipping_method" class="form-label">طريقة الشحن</label>
                                            <select class="form-select" id="shipping_method" name="shipping_method">
                                                <option value="">اختر...</option>
                                                <option value="جوي" <?= $shipment['shipping_method'] === 'جوي' ? 'selected' : '' ?>>جوي</option>
                                                <option value="بري" <?= $shipment['shipping_method'] === 'بري' ? 'selected' : '' ?>>بري</option>
                                            </select>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-3" id="weight_field" style="display: <?= $shipment['package_type'] === 'document' ? 'none' : 'block' ?>;">
                                        <div class="mb-3">
                                            <label for="weight" class="form-label">الوزن (كغ)</label>
                                            <input type="number" 
                                                   class="form-control" 
                                                   id="weight" 
                                                   name="weight" 
                                                   step="0.001" 
                                                   min="0"
                                                   value="<?= number_format($shipment['weight'], 3) ?>">
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-3">
                                        <div class="mb-3">
                                            <label for="status" class="form-label">الحالة</label>
                                            <select class="form-select" id="status" name="status">
                                                <option value="created" <?= $shipment['status'] === 'created' ? 'selected' : '' ?>>تم الإنشاء</option>
                                                <option value="packaged" <?= $shipment['status'] === 'packaged' ? 'selected' : '' ?>>تم التعبئة</option>
                                                <option value="dispatching" <?= $shipment['status'] === 'dispatching' ? 'selected' : '' ?>>في الانتظار للشحن</option>
                                                <option value="shipped" <?= $shipment['status'] === 'shipped' ? 'selected' : '' ?>>تم الشحن</option>
                                                <option value="in_transit" <?= $shipment['status'] === 'in_transit' ? 'selected' : '' ?>>في الطريق</option>
                                                <option value="received" <?= $shipment['status'] === 'received' ? 'selected' : '' ?>>تم الاستلام</option>
                                                <option value="delivered" <?= $shipment['status'] === 'delivered' ? 'selected' : '' ?>>تم التسليم</option>
                                                <option value="cancelled" <?= $shipment['status'] === 'cancelled' ? 'selected' : '' ?>>ملغي</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="mb-3">
                                            <label for="price" class="form-label">السعر الإجمالي (د.ك)</label>
                                            <input type="number" 
                                                   class="form-control" 
                                                   id="price" 
                                                   name="price" 
                                                   step="0.001" 
                                                   min="0"
                                                   value="<?= number_format($shipment['price'], 3) ?>"
                                                   required>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-4">
                                        <div class="mb-3">
                                            <label for="paid_amount" class="form-label">المبلغ المدفوع (د.ك)</label>
                                            <input type="number" 
                                                   class="form-control" 
                                                   id="paid_amount" 
                                                   name="paid_amount" 
                                                   step="0.001" 
                                                   min="0"
                                                   value="<?= number_format($shipment['paid_amount'], 3) ?>"
                                                   onchange="calculateRemaining()">
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-4">
                                        <div class="mb-3">
                                            <label class="form-label">المبلغ المتبقي (د.ك)</label>
                                            <input type="text" 
                                                   class="form-control bg-light" 
                                                   id="remaining_amount"
                                                   value="<?= number_format($shipment['remaining_amount'], 3) ?>" 
                                                   readonly>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row" id="contents_field" style="display: <?= $shipment['package_type'] === 'document' ? 'none' : 'block' ?>;">
                                    <div class="col-12">
                                        <div class="mb-3">
                                            <label for="package_contents" class="form-label">محتويات الطرد</label>
                                            <textarea class="form-control" 
                                                      id="package_contents" 
                                                      name="package_contents" 
                                                      rows="3"><?= htmlspecialchars($shipment['package_contents']) ?></textarea>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-12">
                                        <div class="mb-3">
                                            <label for="notes" class="form-label">ملاحظات</label>
                                            <textarea class="form-control" 
                                                      id="notes" 
                                                      name="notes" 
                                                      rows="3"><?= htmlspecialchars($shipment['notes']) ?></textarea>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Additional Options -->
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-check">
                                            <input class="form-check-input" 
                                                   type="checkbox" 
                                                   id="has_packaging" 
                                                   name="has_packaging"
                                                   <?= $shipment['has_packaging'] ? 'checked' : '' ?>>
                                            <label class="form-check-label" for="has_packaging">
                                                تغليف إضافي
                                            </label>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="waybill_price" class="form-label">سعر بوليصة الشحن (د.ك)</label>
                                            <input type="number" 
                                                   class="form-control" 
                                                   id="waybill_price" 
                                                   name="waybill_price" 
                                                   step="0.001" 
                                                   min="0"
                                                   value="<?= number_format($shipment['waybill_price'], 3) ?>">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Submit Buttons -->
                        <div class="d-flex justify-content-between">
                            <a href="shipments.php" class="btn btn-secondary">
                                <i class="fas fa-times me-2"></i>إلغاء
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>حفظ التغييرات
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function toggleFields() {
    const packageType = document.getElementById('package_type').value;
    const shippingMethodField = document.getElementById('shipping_method_field');
    const weightField = document.getElementById('weight_field');
    const contentsField = document.getElementById('contents_field');
    
    if (packageType === 'document') {
        shippingMethodField.style.display = 'none';
        weightField.style.display = 'none';
        contentsField.style.display = 'none';
    } else {
        shippingMethodField.style.display = 'block';
        weightField.style.display = 'block';
        contentsField.style.display = 'block';
    }
}

function calculateRemaining() {
    const price = parseFloat(document.getElementById('price').value) || 0;
    const paidAmount = parseFloat(document.getElementById('paid_amount').value) || 0;
    const remaining = price - paidAmount;
    
    document.getElementById('remaining_amount').value = remaining.toFixed(3);
}

// Initialize field visibility
document.addEventListener('DOMContentLoaded', function() {
    toggleFields();
});
</script>

<?php include 'views/footer.php'; ?>