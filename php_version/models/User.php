<?php
/**
 * User Model
 * Shipping Management System - PHP Version
 */

class User {
    private $db;
    
    public function __construct() {
        global $db;
        $this->db = $db;
    }
    
    /**
     * Create new user
     */
    public function create($data) {
        $data['password_hash'] = hashPassword($data['password']);
        unset($data['password']);
        $data['created_at'] = date('Y-m-d H:i:s');
        $data['permissions'] = json_encode($data['permissions'] ?? []);
        
        return $this->db->insert('admin', $data);
    }
    
    /**
     * Get user by ID
     */
    public function getById($id) {
        $user = $this->db->fetchOne("SELECT * FROM admin WHERE id = ?", [$id]);
        if ($user) {
            $user['permissions'] = json_decode($user['permissions'] ?? '[]', true);
        }
        return $user;
    }
    
    /**
     * Get user by username
     */
    public function getByUsername($username) {
        $user = $this->db->fetchOne("SELECT * FROM admin WHERE username = ?", [$username]);
        if ($user) {
            $user['permissions'] = json_decode($user['permissions'] ?? '[]', true);
        }
        return $user;
    }
    
    /**
     * Get user by email
     */
    public function getByEmail($email) {
        $user = $this->db->fetchOne("SELECT * FROM admin WHERE email = ?", [$email]);
        if ($user) {
            $user['permissions'] = json_decode($user['permissions'] ?? '[]', true);
        }
        return $user;
    }
    
    /**
     * Get all users
     */
    public function getAll() {
        $users = $this->db->fetchAll("SELECT * FROM admin ORDER BY created_at DESC");
        foreach ($users as &$user) {
            $user['permissions'] = json_decode($user['permissions'] ?? '[]', true);
        }
        return $users;
    }
    
    /**
     * Update user
     */
    public function update($id, $data) {
        if (isset($data['password'])) {
            $data['password_hash'] = hashPassword($data['password']);
            unset($data['password']);
        }
        
        if (isset($data['permissions'])) {
            $data['permissions'] = json_encode($data['permissions']);
        }
        
        return $this->db->update('admin', $data, 'id = ?', [$id]);
    }
    
    /**
     * Delete user
     */
    public function delete($id) {
        return $this->db->delete('admin', 'id = ?', [$id]);
    }
    
    /**
     * Authenticate user
     */
    public function authenticate($username, $password) {
        $user = $this->getByUsername($username);
        
        if ($user && verifyPassword($password, $user['password_hash'])) {
            return $user;
        }
        
        return false;
    }
    
    /**
     * Check if user has permission
     */
    public function hasPermission($userId, $permission) {
        $user = $this->getById($userId);
        
        if (!$user) {
            return false;
        }
        
        if ($user['is_super_admin']) {
            return true;
        }
        
        return in_array($permission, $user['permissions']);
    }
    
    /**
     * Update user permissions
     */
    public function updatePermissions($id, $permissions) {
        return $this->update($id, ['permissions' => $permissions]);
    }
    
    /**
     * Change password
     */
    public function changePassword($id, $newPassword) {
        return $this->update($id, ['password' => $newPassword]);
    }
    
    /**
     * Check if username exists
     */
    public function usernameExists($username, $excludeId = null) {
        $sql = "SELECT COUNT(*) as count FROM admin WHERE username = ?";
        $params = [$username];
        
        if ($excludeId) {
            $sql .= " AND id != ?";
            $params[] = $excludeId;
        }
        
        $result = $this->db->fetchOne($sql, $params);
        return $result['count'] > 0;
    }
    
    /**
     * Check if email exists
     */
    public function emailExists($email, $excludeId = null) {
        $sql = "SELECT COUNT(*) as count FROM admin WHERE email = ?";
        $params = [$email];
        
        if ($excludeId) {
            $sql .= " AND id != ?";
            $params[] = $excludeId;
        }
        
        $result = $this->db->fetchOne($sql, $params);
        return $result['count'] > 0;
    }
    
    /**
     * Get user activity log
     */
    public function getActivityLog($userId, $limit = 50) {
        return $this->db->fetchAll(
            "SELECT * FROM activity_log WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            [$userId, $limit]
        );
    }
    
    /**
     * Update last login
     */
    public function updateLastLogin($id) {
        return $this->update($id, ['last_login' => date('Y-m-d H:i:s')]);
    }
    
    /**
     * Create default admin user
     */
    public function createDefaultAdmin() {
        // Check if admin already exists
        if ($this->getByUsername('admin')) {
            return false;
        }
        
        $adminData = [
            'username' => 'admin',
            'email' => 'admin@shipping.com',
            'password' => 'admin123',
            'is_super_admin' => true,
            'permissions' => [
                'home', 'shipments', 'tracking', 'reports', 
                'expenses', 'add_shipment', 'settings'
            ]
        ];
        
        return $this->create($adminData);
    }
}
?>