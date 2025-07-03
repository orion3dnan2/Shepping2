<?php
/**
 * Print Invoice
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

$shipmentModel = new Shipment();
$shipmentId = intval($_GET['id'] ?? 0);

// Get shipment details
$shipment = $shipmentModel->getById($shipmentId);
if (!$shipment) {
    die('الشحنة غير موجودة');
}
?>

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فاتورة الشحن - <?= htmlspecialchars($shipment['tracking_number']) ?></title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Tajawal', Arial, sans-serif;
            background: white;
            margin: 0;
            padding: 20px;
        }
        
        .invoice-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border: 2px solid #333;
            padding: 30px;
        }
        
        .invoice-header {
            text-align: center;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .company-logo {
            width: 100px;
            height: 100px;
            margin: 0 auto 15px;
            background: #f8f9fa;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #333;
        }
        
        .company-name {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin: 0 0 10px 0;
        }
        
        .invoice-title {
            font-size: 20px;
            font-weight: bold;
            color: #666;
            margin: 0;
        }
        
        .tracking-number {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            background: #f8f9fa;
            padding: 10px;
            border: 2px solid #333;
            margin: 20px 0;
            text-align: center;
        }
        
        .info-section {
            margin-bottom: 25px;
        }
        
        .info-title {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            padding: 8px;
            background: #f8f9fa;
            border: 1px solid #333;
        }
        
        .info-content {
            padding: 15px;
            border: 1px solid #333;
            background: white;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .info-label {
            font-weight: bold;
            color: #333;
        }
        
        .info-value {
            color: #666;
        }
        
        .price-section {
            background: #f8f9fa;
            border: 3px solid #333;
            padding: 20px;
            margin: 30px 0;
            text-align: center;
        }
        
        .total-price {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        
        .signatures {
            display: flex;
            justify-content: space-between;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #333;
        }
        
        .signature-box {
            text-align: center;
            width: 200px;
        }
        
        .signature-line {
            border-bottom: 2px solid #333;
            height: 50px;
            margin-bottom: 10px;
        }
        
        .signature-label {
            font-weight: bold;
            color: #333;
        }
        
        @media print {
            body {
                padding: 0;
            }
            
            .no-print {
                display: none !important;
            }
            
            .invoice-container {
                border: 2px solid #000;
                margin: 0;
                max-width: none;
            }
        }
        
        @media (max-width: 768px) {
            .invoice-container {
                padding: 15px;
            }
            
            .signatures {
                flex-direction: column;
                gap: 30px;
            }
            
            .signature-box {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- Print and Close Buttons -->
    <div class="no-print text-center mb-3">
        <button onclick="window.print()" class="btn btn-primary me-2">
            <i class="fas fa-print me-2"></i>طباعة
        </button>
        <button onclick="window.close()" class="btn btn-secondary">
            <i class="fas fa-times me-2"></i>إغلاق
        </button>
    </div>

    <div class="invoice-container">
        <!-- Invoice Header -->
        <div class="invoice-header">
            <div class="company-logo">
                <i class="fas fa-shipping-fast" style="font-size: 36px; color: #333;"></i>
            </div>
            <h1 class="company-name"><?= APP_NAME ?></h1>
            <h2 class="invoice-title">فاتورة الشحن</h2>
        </div>

        <!-- Tracking Number -->
        <div class="tracking-number">
            رقم التتبع: <?= htmlspecialchars($shipment['tracking_number']) ?>
        </div>

        <!-- Shipment Information -->
        <div class="row">
            <div class="col-md-6">
                <div class="info-section">
                    <div class="info-title">
                        <i class="fas fa-user me-2"></i>معلومات المرسل
                    </div>
                    <div class="info-content">
                        <div class="info-row">
                            <span class="info-label">الاسم:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['sender_name']) ?></span>
                        </div>
                        <?php if ($shipment['sender_phone']): ?>
                        <div class="info-row">
                            <span class="info-label">الهاتف:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['sender_phone']) ?></span>
                        </div>
                        <?php endif; ?>
                        <?php if ($shipment['sender_address']): ?>
                        <div class="info-row">
                            <span class="info-label">العنوان:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['sender_address']) ?></span>
                        </div>
                        <?php endif; ?>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="info-section">
                    <div class="info-title">
                        <i class="fas fa-user-check me-2"></i>معلومات المستلم
                    </div>
                    <div class="info-content">
                        <div class="info-row">
                            <span class="info-label">الاسم:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['receiver_name']) ?></span>
                        </div>
                        <?php if ($shipment['receiver_phone']): ?>
                        <div class="info-row">
                            <span class="info-label">الهاتف:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['receiver_phone']) ?></span>
                        </div>
                        <?php endif; ?>
                        <?php if ($shipment['receiver_address']): ?>
                        <div class="info-row">
                            <span class="info-label">العنوان:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['receiver_address']) ?></span>
                        </div>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>

        <!-- Shipment Details -->
        <div class="info-section">
            <div class="info-title">
                <i class="fas fa-box me-2"></i>تفاصيل الشحنة
            </div>
            <div class="info-content">
                <div class="row">
                    <div class="col-md-6">
                        <div class="info-row">
                            <span class="info-label">نوع الشحنة:</span>
                            <span class="info-value">
                                <?= $shipment['package_type'] === 'document' ? 'مستندات' : 'عامة' ?>
                            </span>
                        </div>
                        
                        <?php if ($shipment['shipping_method']): ?>
                        <div class="info-row">
                            <span class="info-label">طريقة الشحن:</span>
                            <span class="info-value"><?= htmlspecialchars($shipment['shipping_method']) ?></span>
                        </div>
                        <?php endif; ?>
                        
                        <?php if ($shipment['weight'] > 0): ?>
                        <div class="info-row">
                            <span class="info-label">الوزن:</span>
                            <span class="info-value"><?= number_format($shipment['weight'], 3) ?> كغ</span>
                        </div>
                        <?php endif; ?>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="info-row">
                            <span class="info-label">الحالة:</span>
                            <span class="info-value">
                                <?php
                                $statusNames = [
                                    'created' => 'تم الإنشاء',
                                    'packaged' => 'تم التعبئة',
                                    'dispatching' => 'في الانتظار للشحن',
                                    'shipped' => 'تم الشحن',
                                    'in_transit' => 'في الطريق',
                                    'received' => 'تم الاستلام',
                                    'delivered' => 'تم التسليم',
                                    'cancelled' => 'ملغي'
                                ];
                                echo $statusNames[$shipment['status']] ?? $shipment['status'];
                                ?>
                            </span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">تاريخ الإنشاء:</span>
                            <span class="info-value"><?= formatDate($shipment['created_at']) ?></span>
                        </div>
                    </div>
                </div>

                <?php if ($shipment['package_contents']): ?>
                <div class="info-row">
                    <span class="info-label">
                        <?= $shipment['package_type'] === 'document' ? 'الإجراء:' : 'محتويات الطرد:' ?>
                    </span>
                    <span class="info-value"><?= htmlspecialchars($shipment['package_contents']) ?></span>
                </div>
                <?php endif; ?>

                <?php if ($shipment['notes']): ?>
                <div class="info-row">
                    <span class="info-label">ملاحظات:</span>
                    <span class="info-value"><?= htmlspecialchars($shipment['notes']) ?></span>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Price Section -->
        <div class="price-section">
            <div class="info-row mb-3">
                <span class="info-label">السعر الإجمالي:</span>
                <span class="total-price"><?= formatCurrency($shipment['price']) ?></span>
            </div>
            
            <?php if ($shipment['paid_amount'] > 0): ?>
            <div class="info-row mb-2">
                <span class="info-label">المبلغ المدفوع:</span>
                <span class="info-value"><?= formatCurrency($shipment['paid_amount']) ?></span>
            </div>
            <?php endif; ?>
            
            <?php if ($shipment['remaining_amount'] > 0): ?>
            <div class="info-row">
                <span class="info-label">المبلغ المتبقي:</span>
                <span class="info-value text-warning"><?= formatCurrency($shipment['remaining_amount']) ?></span>
            </div>
            <?php endif; ?>
        </div>

        <!-- Signatures -->
        <div class="signatures">
            <div class="signature-box">
                <div class="signature-line"></div>
                <div class="signature-label">توقيع الموظف</div>
            </div>
            
            <div class="signature-box">
                <div class="signature-line"></div>
                <div class="signature-label">توقيع العميل</div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Auto print on load (optional)
        // window.onload = function() { window.print(); }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                window.print();
            }
            if (e.key === 'Escape') {
                window.close();
            }
        });
    </script>
</body>
</html>