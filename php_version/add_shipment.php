<?php
/**
 * Add New Shipment
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

requireLogin();
requirePermission('add_shipment');

$shipmentModel = new Shipment();
$errors = [];
$success = false;

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!verifyCSRFToken($_POST['csrf_token'] ?? '')) {
        $errors[] = 'Invalid request. Please try again.';
    } else {
        // Sanitize and validate input
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
            'notes' => sanitize($_POST['notes'] ?? '')
        ];
        
        // Validation
        if (empty($data['sender_name'])) {
            $errors[] = 'اسم المرسل مطلوب';
        }
        
        if (empty($data['receiver_name'])) {
            $errors[] = 'اسم المستلم مطلوب';
        }
        
        if ($data['weight'] <= 0 && $data['package_type'] !== 'document') {
            $errors[] = 'الوزن مطلوب للشحنات العامة';
        }
        
        if ($data['price'] < 0) {
            $errors[] = 'السعر يجب أن يكون أكبر من الصفر';
        }
        
        if ($data['paid_amount'] > $data['price']) {
            $errors[] = 'المبلغ المدفوع لا يمكن أن يكون أكبر من السعر الإجمالي';
        }
        
        // Phone validation
        if (!empty($data['sender_phone']) && !isValidPhone($data['sender_phone'])) {
            $errors[] = 'رقم هاتف المرسل غير صحيح';
        }
        
        if (!empty($data['receiver_phone']) && !isValidPhone($data['receiver_phone'])) {
            $errors[] = 'رقم هاتف المستلم غير صحيح';
        }
        
        // If no errors, create shipment
        if (empty($errors)) {
            try {
                $shipmentId = $shipmentModel->create($data);
                
                if ($shipmentId) {
                    logActivity('create_shipment', "Created shipment with ID: {$shipmentId}");
                    setFlash('success', 'تم إنشاء الشحنة بنجاح');
                    
                    // Redirect to shipment details or list
                    header('Location: shipments.php');
                    exit;
                } else {
                    $errors[] = 'فشل في إنشاء الشحنة';
                }
            } catch (Exception $e) {
                $errors[] = 'خطأ في قاعدة البيانات: ' . $e->getMessage();
            }
        }
    }
}

// Get zones for dropdown
$zones = [
    'الخرطوم' => 'الخرطوم',
    'أمدرمان' => 'أمدرمان', 
    'الجزيرة' => 'الجزيرة',
    'كسلا' => 'كسلا',
    'بورتسودان' => 'بورتسودان',
    'الشمالية' => 'الشمالية',
    'نهر النيل' => 'نهر النيل',
    'البحر الأحمر' => 'البحر الأحمر',
    'القضارف' => 'القضارف',
    'سنار' => 'سنار'
];

$pageTitle = __('add_shipment');
include 'views/header.php';
?>

<div class="container-fluid py-4">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-plus me-2"></i>
                        <?= __('add_shipment') ?>
                    </h5>
                </div>
                <div class="card-body">
                    <?php if (!empty($errors)): ?>
                    <div class="alert alert-danger">
                        <ul class="mb-0">
                            <?php foreach ($errors as $error): ?>
                            <li><?= htmlspecialchars($error) ?></li>
                            <?php endforeach; ?>
                        </ul>
                    </div>
                    <?php endif; ?>
                    
                    <form method="POST" action="" id="shipmentForm">
                        <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                        
                        <!-- Sender Information -->
                        <div class="row mb-4">
                            <div class="col-12">
                                <h6 class="text-primary mb-3">
                                    <i class="fas fa-user me-2"></i>معلومات المرسل
                                </h6>
                            </div>
                            
                            <div class="col-md-4 mb-3">
                                <label for="sender_name" class="form-label"><?= __('sender_name') ?> *</label>
                                <input type="text" class="form-control" id="sender_name" name="sender_name" 
                                       value="<?= htmlspecialchars($_POST['sender_name'] ?? '') ?>" required>
                            </div>
                            
                            <div class="col-md-4 mb-3">
                                <label for="sender_phone" class="form-label"><?= __('sender_phone') ?></label>
                                <input type="tel" class="form-control" id="sender_phone" name="sender_phone" 
                                       value="<?= htmlspecialchars($_POST['sender_phone'] ?? '') ?>">
                            </div>
                            
                            <div class="col-md-4 mb-3">
                                <label for="sender_address" class="form-label"><?= __('sender_address') ?></label>
                                <input type="text" class="form-control" id="sender_address" name="sender_address" 
                                       value="<?= htmlspecialchars($_POST['sender_address'] ?? '') ?>">
                            </div>
                        </div>
                        
                        <!-- Receiver Information -->
                        <div class="row mb-4">
                            <div class="col-12">
                                <h6 class="text-success mb-3">
                                    <i class="fas fa-user-check me-2"></i>معلومات المستلم
                                </h6>
                            </div>
                            
                            <div class="col-md-4 mb-3">
                                <label for="receiver_name" class="form-label"><?= __('receiver_name') ?> *</label>
                                <input type="text" class="form-control" id="receiver_name" name="receiver_name" 
                                       value="<?= htmlspecialchars($_POST['receiver_name'] ?? '') ?>" required>
                            </div>
                            
                            <div class="col-md-4 mb-3">
                                <label for="receiver_phone" class="form-label"><?= __('receiver_phone') ?></label>
                                <input type="tel" class="form-control" id="receiver_phone" name="receiver_phone" 
                                       value="<?= htmlspecialchars($_POST['receiver_phone'] ?? '') ?>">
                            </div>
                            
                            <div class="col-md-4 mb-3">
                                <label for="receiver_address" class="form-label"><?= __('receiver_address') ?></label>
                                <input type="text" class="form-control" id="receiver_address" name="receiver_address" 
                                       value="<?= htmlspecialchars($_POST['receiver_address'] ?? '') ?>">
                            </div>
                        </div>
                        
                        <!-- Shipment Details -->
                        <div class="row mb-4">
                            <div class="col-12">
                                <h6 class="text-info mb-3">
                                    <i class="fas fa-box me-2"></i>تفاصيل الشحنة
                                </h6>
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <label for="package_type" class="form-label"><?= __('package_type') ?></label>
                                <select class="form-select" id="package_type" name="package_type" onchange="toggleFields()">
                                    <option value="general" <?= ($_POST['package_type'] ?? '') === 'general' ? 'selected' : '' ?>>عامة</option>
                                    <option value="document" <?= ($_POST['package_type'] ?? '') === 'document' ? 'selected' : '' ?>>مستندات</option>
                                </select>
                            </div>
                            
                            <div class="col-md-3 mb-3" id="shipping_method_group">
                                <label for="shipping_method" class="form-label"><?= __('shipping_method') ?></label>
                                <select class="form-select" id="shipping_method" name="shipping_method">
                                    <option value="">اختر طريقة الشحن</option>
                                    <option value="جوي" <?= ($_POST['shipping_method'] ?? '') === 'جوي' ? 'selected' : '' ?>>جوي</option>
                                    <option value="بري" <?= ($_POST['shipping_method'] ?? '') === 'بري' ? 'selected' : '' ?>>بري</option>
                                </select>
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <label for="zone" class="form-label"><?= __('zone') ?></label>
                                <select class="form-select" id="zone" name="zone">
                                    <option value="">اختر المنطقة</option>
                                    <?php foreach ($zones as $value => $label): ?>
                                    <option value="<?= $value ?>" <?= ($_POST['zone'] ?? '') === $value ? 'selected' : '' ?>><?= $label ?></option>
                                    <?php endforeach; ?>
                                </select>
                            </div>
                            
                            <div class="col-md-3 mb-3" id="weight_group">
                                <label for="weight" class="form-label"><?= __('weight') ?> (كغ)</label>
                                <input type="number" step="0.001" class="form-control" id="weight" name="weight" 
                                       value="<?= $_POST['weight'] ?? '' ?>" onchange="calculatePrice()">
                            </div>
                        </div>
                        
                        <!-- Package Contents -->
                        <div class="row mb-4" id="contents_group">
                            <div class="col-md-6 mb-3">
                                <label for="package_contents" class="form-label"><?= __('package_contents') ?></label>
                                <textarea class="form-control" id="package_contents" name="package_contents" rows="3"><?= htmlspecialchars($_POST['package_contents'] ?? '') ?></textarea>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="notes" class="form-label"><?= __('notes') ?></label>
                                <textarea class="form-control" id="notes" name="notes" rows="3"><?= htmlspecialchars($_POST['notes'] ?? '') ?></textarea>
                            </div>
                        </div>
                        
                        <!-- Pricing -->
                        <div class="row mb-4">
                            <div class="col-12">
                                <h6 class="text-warning mb-3">
                                    <i class="fas fa-dollar-sign me-2"></i>التسعير
                                </h6>
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <label for="price" class="form-label"><?= __('price') ?> (د.ك)</label>
                                <input type="number" step="0.001" class="form-control" id="price" name="price" 
                                       value="<?= $_POST['price'] ?? '' ?>" onchange="calculateRemaining()">
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <label for="paid_amount" class="form-label"><?= __('paid_amount') ?> (د.ك)</label>
                                <input type="number" step="0.001" class="form-control" id="paid_amount" name="paid_amount" 
                                       value="<?= $_POST['paid_amount'] ?? '' ?>" onchange="calculateRemaining()">
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <label for="remaining_amount" class="form-label"><?= __('remaining_amount') ?> (د.ك)</label>
                                <input type="number" step="0.001" class="form-control" id="remaining_amount" name="remaining_amount" 
                                       value="<?= calculateRemainingAmount($_POST['price'] ?? 0, $_POST['paid_amount'] ?? 0) ?>" readonly>
                            </div>
                            
                            <div class="col-md-3 mb-3">
                                <div class="form-check mt-4">
                                    <input class="form-check-input" type="checkbox" id="has_packaging" name="has_packaging" 
                                           <?= isset($_POST['has_packaging']) ? 'checked' : '' ?>>
                                    <label class="form-check-label" for="has_packaging">
                                        <?= __('packaging') ?>
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Waybill Price (conditional) -->
                        <div class="row mb-4" id="waybill_group" style="display: none;">
                            <div class="col-md-4 mb-3">
                                <label for="waybill_price" class="form-label">سعر بوليصة الشحن (د.ك)</label>
                                <input type="number" step="0.001" class="form-control" id="waybill_price" name="waybill_price" 
                                       value="<?= $_POST['waybill_price'] ?? '' ?>">
                            </div>
                        </div>
                        
                        <!-- Submit Buttons -->
                        <div class="row">
                            <div class="col-12">
                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-primary">
                                        <i class="fas fa-save me-2"></i><?= __('save') ?>
                                    </button>
                                    <a href="shipments.php" class="btn btn-secondary">
                                        <i class="fas fa-times me-2"></i><?= __('cancel') ?>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Toggle fields based on package type
function toggleFields() {
    const packageType = document.getElementById('package_type').value;
    const weightGroup = document.getElementById('weight_group');
    const contentsGroup = document.getElementById('contents_group');
    const shippingMethodGroup = document.getElementById('shipping_method_group');
    
    if (packageType === 'document') {
        weightGroup.style.display = 'none';
        contentsGroup.style.display = 'none';
        shippingMethodGroup.style.display = 'none';
        
        // Clear required attributes
        document.getElementById('weight').removeAttribute('required');
    } else {
        weightGroup.style.display = 'block';
        contentsGroup.style.display = 'block';
        shippingMethodGroup.style.display = 'block';
        
        // Add required attributes
        document.getElementById('weight').setAttribute('required', 'required');
    }
}

// Calculate remaining amount
function calculateRemaining() {
    const priceInput = document.getElementById('price');
    const paidInput = document.getElementById('paid_amount');
    const remainingInput = document.getElementById('remaining_amount');
    
    calculateRemaining(priceInput, paidInput, remainingInput);
}

// Initialize form
document.addEventListener('DOMContentLoaded', function() {
    toggleFields();
});
</script>

<?php include 'views/footer.php'; ?>