<?php
/**
 * System Settings
 * Shipping Management System - PHP Version
 */

require_once 'config/config.php';

requireLogin();
requirePermission('settings');

$userModel = new User();

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (verifyCSRFToken($_POST['csrf_token'] ?? '')) {
        $action = $_POST['action'] ?? '';
        
        switch ($action) {
            case 'add_user':
                $userData = [
                    'username' => sanitize($_POST['username'] ?? ''),
                    'email' => sanitize($_POST['email'] ?? ''),
                    'password' => $_POST['password'] ?? '',
                    'is_super_admin' => isset($_POST['is_super_admin']),
                    'permissions' => $_POST['permissions'] ?? []
                ];
                
                if ($userModel->create($userData)) {
                    logActivity('add_user', "Created user: {$userData['username']}");
                    setFlash('success', 'تم إضافة المستخدم بنجاح');
                } else {
                    setFlash('error', 'فشل في إضافة المستخدم');
                }
                break;
                
            case 'edit_user':
                $userId = intval($_POST['user_id'] ?? 0);
                $userData = [
                    'username' => sanitize($_POST['username'] ?? ''),
                    'email' => sanitize($_POST['email'] ?? ''),
                    'is_super_admin' => isset($_POST['is_super_admin']),
                    'permissions' => $_POST['permissions'] ?? []
                ];
                
                // Only update password if provided
                if (!empty($_POST['password'])) {
                    $userData['password'] = $_POST['password'];
                }
                
                if ($userModel->update($userId, $userData)) {
                    logActivity('edit_user', "Updated user ID: {$userId}");
                    setFlash('success', 'تم تحديث المستخدم بنجاح');
                } else {
                    setFlash('error', 'فشل في تحديث المستخدم');
                }
                break;
                
            case 'delete_user':
                $userId = intval($_POST['user_id'] ?? 0);
                if ($userId !== $_SESSION['user_id']) {  // Prevent self-deletion
                    if ($userModel->delete($userId)) {
                        logActivity('delete_user', "Deleted user ID: {$userId}");
                        setFlash('success', 'تم حذف المستخدم بنجاح');
                    } else {
                        setFlash('error', 'فشل في حذف المستخدم');
                    }
                } else {
                    setFlash('error', 'لا يمكنك حذف حسابك الخاص');
                }
                break;
        }
        
        header('Location: settings.php');
        exit;
    }
}

// Get all users
$users = $userModel->getAll();
$permissions = ['home', 'shipments', 'tracking', 'reports', 'expenses', 'add_shipment', 'settings'];

$pageTitle = 'الإعدادات';
include 'views/header.php';
?>

<div class="container-fluid py-4">
    <!-- Settings Navigation Tabs -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-cog me-2"></i>إعدادات النظام
                    </h6>
                </div>
                <div class="card-body">
                    <ul class="nav nav-pills mb-4" id="settingsTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="users-tab" data-bs-toggle="pill" data-bs-target="#users" type="button" role="tab">
                                <i class="fas fa-users me-2"></i>إدارة المستخدمين
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="system-tab" data-bs-toggle="pill" data-bs-target="#system" type="button" role="tab">
                                <i class="fas fa-server me-2"></i>إعدادات النظام
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="backup-tab" data-bs-toggle="pill" data-bs-target="#backup" type="button" role="tab">
                                <i class="fas fa-database me-2"></i>النسخ الاحتياطي
                            </button>
                        </li>
                    </ul>

                    <div class="tab-content" id="settingsTabsContent">
                        <!-- Users Management Tab -->
                        <div class="tab-pane fade show active" id="users" role="tabpanel">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h6 class="mb-0">قائمة المستخدمين</h6>
                                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addUserModal">
                                    <i class="fas fa-user-plus me-2"></i>إضافة مستخدم جديد
                                </button>
                            </div>

                            <div class="table-responsive">
                                <table class="table align-items-center mb-0">
                                    <thead>
                                        <tr>
                                            <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">المستخدم</th>
                                            <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">الصلاحيات</th>
                                            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">النوع</th>
                                            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">آخر دخول</th>
                                            <th class="text-secondary opacity-7">الإجراءات</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($users as $user): ?>
                                        <tr>
                                            <td>
                                                <div class="d-flex px-2 py-1">
                                                    <div class="d-flex flex-column justify-content-center">
                                                        <h6 class="mb-0 text-sm"><?= htmlspecialchars($user['username']) ?></h6>
                                                        <p class="text-xs text-secondary mb-0"><?= htmlspecialchars($user['email']) ?></p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                <?php 
                                                $userPermissions = json_decode($user['permissions'], true) ?? [];
                                                foreach (array_slice($userPermissions, 0, 3) as $permission): ?>
                                                    <span class="badge bg-success me-1"><?= $permission ?></span>
                                                <?php endforeach; ?>
                                                <?php if (count($userPermissions) > 3): ?>
                                                    <span class="badge bg-info">+<?= count($userPermissions) - 3 ?></span>
                                                <?php endif; ?>
                                            </td>
                                            <td class="align-middle text-center">
                                                <?php if ($user['is_super_admin']): ?>
                                                    <span class="badge bg-danger">مدير عام</span>
                                                <?php else: ?>
                                                    <span class="badge bg-secondary">مستخدم</span>
                                                <?php endif; ?>
                                            </td>
                                            <td class="align-middle text-center">
                                                <span class="text-secondary text-xs font-weight-bold">
                                                    <?= $user['last_login'] ? formatDate($user['last_login']) : 'لم يسجل دخول' ?>
                                                </span>
                                            </td>
                                            <td class="align-middle">
                                                <div class="d-flex gap-1">
                                                    <button onclick="editUser(<?= htmlspecialchars(json_encode($user)) ?>)" 
                                                            class="btn btn-outline-primary btn-sm" title="تعديل">
                                                        <i class="fas fa-edit"></i>
                                                    </button>
                                                    
                                                    <?php if ($user['id'] !== $_SESSION['user_id']): ?>
                                                    <button onclick="deleteUser(<?= $user['id'] ?>)" 
                                                            class="btn btn-outline-danger btn-sm" title="حذف">
                                                        <i class="fas fa-trash"></i>
                                                    </button>
                                                    <?php endif; ?>
                                                </div>
                                            </td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- System Settings Tab -->
                        <div class="tab-pane fade" id="system" role="tabpanel">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">إعدادات عامة</h6>
                                        </div>
                                        <div class="card-body">
                                            <form>
                                                <div class="mb-3">
                                                    <label class="form-label">اسم الشركة</label>
                                                    <input type="text" class="form-control" value="<?= APP_NAME ?>" readonly>
                                                </div>
                                                <div class="mb-3">
                                                    <label class="form-label">إصدار النظام</label>
                                                    <input type="text" class="form-control" value="PHP Version 2.0.0" readonly>
                                                </div>
                                                <div class="mb-3">
                                                    <label class="form-label">قاعدة البيانات</label>
                                                    <input type="text" class="form-control" value="MySQL" readonly>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">إحصائيات النظام</h6>
                                        </div>
                                        <div class="card-body">
                                            <?php 
                                            $shipmentModel = new Shipment();
                                            $totalShipments = count($shipmentModel->getAll(1, 999999));
                                            $totalUsers = count($users);
                                            ?>
                                            <div class="mb-3">
                                                <div class="d-flex justify-content-between">
                                                    <span>إجمالي الشحنات</span>
                                                    <span class="badge bg-primary"><?= $totalShipments ?></span>
                                                </div>
                                            </div>
                                            <div class="mb-3">
                                                <div class="d-flex justify-content-between">
                                                    <span>إجمالي المستخدمين</span>
                                                    <span class="badge bg-success"><?= $totalUsers ?></span>
                                                </div>
                                            </div>
                                            <div class="mb-3">
                                                <div class="d-flex justify-content-between">
                                                    <span>حالة النظام</span>
                                                    <span class="badge bg-success">يعمل</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Backup Tab -->
                        <div class="tab-pane fade" id="backup" role="tabpanel">
                            <div class="row">
                                <div class="col-md-8">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">النسخ الاحتياطي</h6>
                                        </div>
                                        <div class="card-body">
                                            <div class="alert alert-info">
                                                <i class="fas fa-info-circle me-2"></i>
                                                يُنصح بعمل نسخة احتياطية من قاعدة البيانات بانتظام للحفاظ على البيانات.
                                            </div>
                                            
                                            <div class="d-grid gap-2">
                                                <button class="btn btn-primary" onclick="alert('تواصل مع مدير النظام لعمل نسخة احتياطية')">
                                                    <i class="fas fa-download me-2"></i>تصدير النسخة الاحتياطية
                                                </button>
                                                <button class="btn btn-warning" onclick="alert('تواصل مع مدير النظام لاستيراد نسخة احتياطية')">
                                                    <i class="fas fa-upload me-2"></i>استيراد نسخة احتياطية
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Add User Modal -->
<div class="modal fade" id="addUserModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">إضافة مستخدم جديد</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST">
                <div class="modal-body">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    <input type="hidden" name="action" value="add_user">
                    
                    <div class="mb-3">
                        <label for="username" class="form-label">اسم المستخدم</label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="email" class="form-label">البريد الإلكتروني</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="password" class="form-label">كلمة المرور</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="is_super_admin" name="is_super_admin">
                            <label class="form-check-label" for="is_super_admin">
                                مدير عام
                            </label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">الصلاحيات</label>
                        <div class="row">
                            <?php foreach ($permissions as $permission): ?>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" 
                                           id="perm_<?= $permission ?>" name="permissions[]" value="<?= $permission ?>">
                                    <label class="form-check-label" for="perm_<?= $permission ?>">
                                        <?= $permission ?>
                                    </label>
                                </div>
                            </div>
                            <?php endforeach; ?>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
                    <button type="submit" class="btn btn-primary">إضافة</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Edit User Modal -->
<div class="modal fade" id="editUserModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">تعديل المستخدم</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST">
                <div class="modal-body">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    <input type="hidden" name="action" value="edit_user">
                    <input type="hidden" name="user_id" id="edit_user_id">
                    
                    <div class="mb-3">
                        <label for="edit_username" class="form-label">اسم المستخدم</label>
                        <input type="text" class="form-control" id="edit_username" name="username" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="edit_email" class="form-label">البريد الإلكتروني</label>
                        <input type="email" class="form-control" id="edit_email" name="email" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="edit_password" class="form-label">كلمة المرور (اتركها فارغة لعدم التغيير)</label>
                        <input type="password" class="form-control" id="edit_password" name="password">
                    </div>
                    
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="edit_is_super_admin" name="is_super_admin">
                            <label class="form-check-label" for="edit_is_super_admin">
                                مدير عام
                            </label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">الصلاحيات</label>
                        <div class="row" id="edit_permissions">
                            <?php foreach ($permissions as $permission): ?>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" 
                                           id="edit_perm_<?= $permission ?>" name="permissions[]" value="<?= $permission ?>">
                                    <label class="form-check-label" for="edit_perm_<?= $permission ?>">
                                        <?= $permission ?>
                                    </label>
                                </div>
                            </div>
                            <?php endforeach; ?>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
                    <button type="submit" class="btn btn-primary">حفظ التغييرات</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Delete User Modal -->
<div class="modal fade" id="deleteUserModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">تأكيد الحذف</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                هل أنت متأكد من حذف هذا المستخدم؟ لا يمكن التراجع عن هذا الإجراء.
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    <input type="hidden" name="action" value="delete_user">
                    <input type="hidden" name="user_id" id="delete_user_id">
                    <button type="submit" class="btn btn-danger">حذف</button>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
function editUser(user) {
    document.getElementById('edit_user_id').value = user.id;
    document.getElementById('edit_username').value = user.username;
    document.getElementById('edit_email').value = user.email;
    document.getElementById('edit_is_super_admin').checked = user.is_super_admin == 1;
    
    // Clear all permission checkboxes
    document.querySelectorAll('#edit_permissions input[type="checkbox"]').forEach(cb => cb.checked = false);
    
    // Set user permissions
    const userPermissions = JSON.parse(user.permissions || '[]');
    userPermissions.forEach(permission => {
        const checkbox = document.getElementById('edit_perm_' + permission);
        if (checkbox) checkbox.checked = true;
    });
    
    new bootstrap.Modal(document.getElementById('editUserModal')).show();
}

function deleteUser(userId) {
    document.getElementById('delete_user_id').value = userId;
    new bootstrap.Modal(document.getElementById('deleteUserModal')).show();
}
</script>

<?php include 'views/footer.php'; ?>