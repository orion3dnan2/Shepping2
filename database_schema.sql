-- MySQL Database Schema for Shipping Management System
-- Run this script to create the database structure

-- Create Database (run this manually in cPanel MySQL)
-- CREATE DATABASE shipping_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
-- USE shipping_system;

-- Admin Users Table
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    is_super_admin BOOLEAN DEFAULT FALSE,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Shipments Table
CREATE TABLE shipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(50) NOT NULL UNIQUE,
    sender_name VARCHAR(100) NOT NULL,
    sender_phone VARCHAR(20),
    sender_address TEXT,
    receiver_name VARCHAR(100) NOT NULL,
    receiver_phone VARCHAR(20),
    receiver_address TEXT,
    direction VARCHAR(20) DEFAULT 'kuwait_to_sudan',
    region VARCHAR(50),
    package_type VARCHAR(50) DEFAULT 'general',
    shipping_method VARCHAR(20),
    weight DECIMAL(10,3),
    price DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    cost DECIMAL(10,3) DEFAULT 0.000,
    paid_amount DECIMAL(10,3) DEFAULT 0.000,
    remaining_amount DECIMAL(10,3) DEFAULT 0.000,
    package_contents TEXT,
    zone VARCHAR(50),
    has_packaging BOOLEAN DEFAULT FALSE,
    waybill_price DECIMAL(10,3) DEFAULT 0.000,
    status VARCHAR(50) DEFAULT 'created',
    sender_latitude DECIMAL(10,8),
    sender_longitude DECIMAL(11,8),
    receiver_latitude DECIMAL(10,8),
    receiver_longitude DECIMAL(11,8),
    current_latitude DECIMAL(10,8),
    current_longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Shipment Types Table
CREATE TABLE shipment_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    price_per_kg DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Document Types Table
CREATE TABLE document_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    price DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Zone Pricing Table
CREATE TABLE zone_pricing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    price_per_kg DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Packaging Types Table
CREATE TABLE packaging_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    price DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Global Settings Table
CREATE TABLE global_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(100) NOT NULL UNIQUE,
    setting_value DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Financial Transactions Table
CREATE TABLE financial_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_type VARCHAR(20) NOT NULL, -- 'expense' or 'revenue'
    revenue_type VARCHAR(50), -- for revenues: 'general_shipments', 'documents', 'other'
    shipping_type VARCHAR(50), -- for expenses: 'general_shipments', 'documents'
    name VARCHAR(200) NOT NULL,
    amount DECIMAL(10,3) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Notifications Table
CREATE TABLE notification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    tracking_number VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert Default Admin User
INSERT INTO admin (username, email, password_hash, is_super_admin, permissions) VALUES (
    'admin',
    'admin@shipping.com',
    'scrypt:32768:8:1$5K6QXgHH3bXQdDfE$308c5b6e7b6a9f8c1e2b3a4d5f6789abc0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5',
    TRUE,
    '{"home": true, "shipments": true, "tracking": true, "reports": true, "expenses": true, "add_shipment": true, "settings": true}'
);

-- Insert Sample Shipment Types
INSERT INTO shipment_type (name_ar, name_en, price_per_kg) VALUES
('إلكترونيات', 'Electronics', 5.000),
('ملابس', 'Clothes', 3.000),
('كتب', 'Books', 2.000),
('أدوية', 'Medicine', 8.000),
('طعام', 'Food', 4.000),
('عامة', 'General', 3.500);

-- Insert Sample Document Types
INSERT INTO document_type (name_ar, name_en, price) VALUES
('الشهادات الرسمية', 'Official Certificates', 25.000),
('الأوراق العامة', 'General Documents', 15.000),
('التوثيقات القانونية', 'Legal Documents', 35.000),
('الأوراق الطبية', 'Medical Documents', 20.000),
('أوراق التعليم', 'Educational Documents', 30.000);

-- Insert Sample Zone Pricing
INSERT INTO zone_pricing (zone_name, price_per_kg) VALUES
('الخرطوم', 5.000),
('أمدرمان', 5.000),
('الجزيرة', 4.500),
('كسلا', 6.000),
('بورتسودان', 7.000),
('الشمالية', 6.500),
('نهر النيل', 6.000),
('البحر الأحمر', 7.500),
('القضارف', 5.500),
('سنار', 5.000);

-- Insert Sample Packaging Types
INSERT INTO packaging_type (name_ar, name_en, price) VALUES
('صندوق عادي', 'Standard Box', 2.000),
('صندوق قوي', 'Strong Box', 3.500),
('مغلف', 'Envelope', 1.000),
('بدون تغليف', 'No Packaging', 0.000);

-- Insert Global Settings
INSERT INTO global_settings (setting_name, setting_value) VALUES
('packaging_price', 2.500),
('waybill_price', 1.500),
('comment_price', 0.500),
('price_per_kg', 4.000);

-- Create Indexes for better performance
CREATE INDEX idx_shipment_tracking ON shipment(tracking_number);
CREATE INDEX idx_shipment_status ON shipment(status);
CREATE INDEX idx_shipment_created ON shipment(created_at);
CREATE INDEX idx_notification_read ON notification(is_read);
CREATE INDEX idx_financial_type ON financial_transaction(transaction_type);
CREATE INDEX idx_financial_date ON financial_transaction(transaction_date);