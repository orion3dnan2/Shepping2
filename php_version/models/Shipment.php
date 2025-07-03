<?php
/**
 * Shipment Model
 * Shipping Management System - PHP Version
 */

class Shipment {
    private $db;
    
    public function __construct() {
        global $db;
        $this->db = $db;
    }
    
    /**
     * Create new shipment
     */
    public function create($data) {
        // Generate tracking number if not provided
        if (empty($data['tracking_number'])) {
            $data['tracking_number'] = $this->generateUniqueTrackingNumber();
        }
        
        // Set default values
        $data['status'] = $data['status'] ?? 'created';
        $data['created_at'] = date('Y-m-d H:i:s');
        $data['remaining_amount'] = ($data['price'] ?? 0) - ($data['paid_amount'] ?? 0);
        
        return $this->db->insert('shipment', $data);
    }
    
    /**
     * Get shipment by ID
     */
    public function getById($id) {
        return $this->db->fetchOne("SELECT * FROM shipment WHERE id = ?", [$id]);
    }
    
    /**
     * Get shipment by tracking number
     */
    public function getByTrackingNumber($trackingNumber) {
        return $this->db->fetchOne("SELECT * FROM shipment WHERE tracking_number = ?", [$trackingNumber]);
    }
    
    /**
     * Get all shipments with pagination
     */
    public function getAll($page = 1, $limit = 50, $filters = []) {
        $offset = ($page - 1) * $limit;
        $where = [];
        $params = [];
        
        // Apply filters
        if (!empty($filters['status'])) {
            $where[] = "status = ?";
            $params[] = $filters['status'];
        }
        
        if (!empty($filters['package_type'])) {
            $where[] = "package_type = ?";
            $params[] = $filters['package_type'];
        }
        
        if (!empty($filters['shipping_method'])) {
            $where[] = "shipping_method = ?";
            $params[] = $filters['shipping_method'];
        }
        
        if (!empty($filters['date_from'])) {
            $where[] = "DATE(created_at) >= ?";
            $params[] = $filters['date_from'];
        }
        
        if (!empty($filters['date_to'])) {
            $where[] = "DATE(created_at) <= ?";
            $params[] = $filters['date_to'];
        }
        
        $whereClause = !empty($where) ? "WHERE " . implode(" AND ", $where) : "";
        
        $sql = "SELECT * FROM shipment {$whereClause} ORDER BY created_at DESC LIMIT {$limit} OFFSET {$offset}";
        
        return $this->db->fetchAll($sql, $params);
    }
    
    /**
     * Update shipment
     */
    public function update($id, $data) {
        $data['updated_at'] = date('Y-m-d H:i:s');
        
        // Recalculate remaining amount if price or paid_amount changed
        if (isset($data['price']) || isset($data['paid_amount'])) {
            $current = $this->getById($id);
            if ($current) {
                $price = $data['price'] ?? $current['price'];
                $paidAmount = $data['paid_amount'] ?? $current['paid_amount'];
                $data['remaining_amount'] = max(0, $price - $paidAmount);
            }
        }
        
        return $this->db->update('shipment', $data, 'id = ?', [$id]);
    }
    
    /**
     * Delete shipment
     */
    public function delete($id) {
        return $this->db->delete('shipment', 'id = ?', [$id]);
    }
    
    /**
     * Update shipment status
     */
    public function updateStatus($id, $status) {
        return $this->update($id, ['status' => $status]);
    }
    
    /**
     * Process payment
     */
    public function processPayment($id, $amount) {
        $shipment = $this->getById($id);
        if (!$shipment) {
            return false;
        }
        
        $newPaidAmount = $shipment['paid_amount'] + $amount;
        $remainingAmount = max(0, $shipment['price'] - $newPaidAmount);
        
        return $this->update($id, [
            'paid_amount' => $newPaidAmount,
            'remaining_amount' => $remainingAmount
        ]);
    }
    
    /**
     * Get recent shipments
     */
    public function getRecent($limit = 10) {
        return $this->db->fetchAll("SELECT * FROM shipment ORDER BY created_at DESC LIMIT ?", [$limit]);
    }
    
    /**
     * Get shipments by status
     */
    public function getByStatus($status) {
        return $this->db->fetchAll("SELECT * FROM shipment WHERE status = ? ORDER BY created_at DESC", [$status]);
    }
    
    /**
     * Search shipments
     */
    public function search($query) {
        $sql = "SELECT * FROM shipment WHERE 
                tracking_number LIKE ? OR 
                sender_name LIKE ? OR 
                receiver_name LIKE ? OR 
                sender_phone LIKE ? OR 
                receiver_phone LIKE ?
                ORDER BY created_at DESC";
        
        $searchTerm = "%{$query}%";
        return $this->db->fetchAll($sql, [$searchTerm, $searchTerm, $searchTerm, $searchTerm, $searchTerm]);
    }
    
    /**
     * Get statistics
     */
    public function getStatistics($dateFrom = null, $dateTo = null) {
        $whereClause = "";
        $params = [];
        
        if ($dateFrom && $dateTo) {
            $whereClause = "WHERE DATE(created_at) BETWEEN ? AND ?";
            $params = [$dateFrom, $dateTo];
        }
        
        $stats = [];
        
        // Total shipments
        $stats['total'] = $this->db->fetchOne("SELECT COUNT(*) as count FROM shipment {$whereClause}", $params)['count'];
        
        // By status
        $statusStats = $this->db->fetchAll("SELECT status, COUNT(*) as count FROM shipment {$whereClause} GROUP BY status", $params);
        foreach ($statusStats as $stat) {
            $stats['status'][$stat['status']] = $stat['count'];
        }
        
        // Revenue
        $revenue = $this->db->fetchOne("SELECT SUM(price) as total_revenue, SUM(paid_amount) as paid_revenue FROM shipment {$whereClause}", $params);
        $stats['revenue'] = $revenue;
        
        // By shipping method
        $methodStats = $this->db->fetchAll("SELECT shipping_method, COUNT(*) as count FROM shipment {$whereClause} GROUP BY shipping_method", $params);
        foreach ($methodStats as $stat) {
            $stats['shipping_method'][$stat['shipping_method']] = $stat['count'];
        }
        
        return $stats;
    }
    
    /**
     * Generate unique tracking number
     */
    private function generateUniqueTrackingNumber() {
        do {
            $trackingNumber = generateTrackingNumber();
            $exists = $this->getByTrackingNumber($trackingNumber);
        } while ($exists);
        
        return $trackingNumber;
    }
    
    /**
     * Get unpaid shipments
     */
    public function getUnpaid() {
        return $this->db->fetchAll("SELECT * FROM shipment WHERE remaining_amount > 0 ORDER BY created_at DESC");
    }
    
    /**
     * Get revenue by shipping method
     */
    public function getRevenueByShippingMethod($method, $dateFrom = null, $dateTo = null) {
        $whereClause = "WHERE shipping_method = ?";
        $params = [$method];
        
        if ($dateFrom && $dateTo) {
            $whereClause .= " AND DATE(created_at) BETWEEN ? AND ?";
            $params[] = $dateFrom;
            $params[] = $dateTo;
        }
        
        return $this->db->fetchAll("SELECT * FROM shipment {$whereClause} ORDER BY created_at DESC", $params);
    }
    
    /**
     * Get document shipments revenue
     */
    public function getDocumentShipmentsRevenue($dateFrom = null, $dateTo = null) {
        $whereClause = "WHERE package_type = 'document'";
        $params = [];
        
        if ($dateFrom && $dateTo) {
            $whereClause .= " AND DATE(created_at) BETWEEN ? AND ?";
            $params = [$dateFrom, $dateTo];
        }
        
        return $this->db->fetchAll("SELECT * FROM shipment {$whereClause} ORDER BY created_at DESC", $params);
    }
}
?>