#!/usr/bin/env python3
"""
Database initialization script for the Shipping Management System
This script creates all necessary tables and populates them with initial data
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import (
    Admin, ShipmentType, DocumentType, ProcedureType, 
    ZonePricing, PackagingType, GlobalSettings, 
    AirShippingCosts, DocumentCosts
)
from datetime import datetime

def initialize_database():
    """Initialize the database with all required tables and initial data"""
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Create default admin user
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin()
            admin.username = 'admin'
            admin.is_super_admin = True
            admin.set_password('admin123')
            admin.set_permissions({
                'home': True,
                'shipments': True,
                'tracking': True,
                'reports': True,
                'expenses': True,
                'add_shipment': True,
                'settings': True
            })
            db.session.add(admin)
            print("✓ Default admin user created (admin/admin123)")
        
        # Create shipment types
        shipment_types_data = [
            ('شحن عام', 'General Shipping', 0.0),
            ('وثائق', 'Documents', 0.0),
            ('طرود', 'Packages', 0.0),
            ('بضائع تجارية', 'Commercial Goods', 0.0),
            ('إلكترونيات', 'Electronics', 0.0),
            ('طعام ومشروبات', 'Food & Beverages', 0.0),
            ('ملابس', 'Clothing', 0.0),
            ('أدوية', 'Medicines', 0.0),
            ('كتب', 'Books', 0.0)
        ]
        
        for name_ar, name_en, price in shipment_types_data:
            existing = ShipmentType.query.filter_by(name_ar=name_ar).first()
            if not existing:
                shipment_type = ShipmentType(
                    name_ar=name_ar,
                    name_en=name_en,
                    price=price,
                    is_active=True
                )
                db.session.add(shipment_type)
        
        print("✓ Shipment types initialized")
        
        # Create document types
        document_types_data = [
            ('توثيق خارجية', 'Foreign Affairs Authentication', 50.0),
            ('توثيق تعليم عالي', 'Higher Education Authentication', 30.0),
            ('أدلة جنائية', 'Criminal Record', 25.0),
            ('شهادة ثانوية', 'Secondary Certificate', 40.0),
            ('شهادة جامعية', 'University Certificate', 60.0),
            ('قسيمة زواج مدرجة', 'Registered Marriage Certificate', 35.0),
            ('قسيمة زواج غير مدرجة', 'Unregistered Marriage Certificate', 45.0),
            ('شهادة جامعية تفاصيل', 'University Certificate Details', 70.0),
            ('شهادة ميلاد', 'Birth Certificate', 20.0),
            ('شهادة وفاة', 'Death Certificate', 20.0),
            ('جواز سفر', 'Passport', 80.0),
            ('رخصة قيادة', 'Driving License', 30.0),
            ('شهادة عسكرية', 'Military Certificate', 40.0)
        ]
        
        for name_ar, name_en, price in document_types_data:
            existing = DocumentType.query.filter_by(name_ar=name_ar).first()
            if not existing:
                document_type = DocumentType(
                    name_ar=name_ar,
                    name_en=name_en,
                    price=price,
                    is_active=True
                )
                db.session.add(document_type)
        
        print("✓ Document types initialized")
        
        # Create procedure types
        procedure_types_data = [
            ('استخراج شهادة ثانوية', 'Secondary Certificate Extraction', 40.0),
            ('استخراج شهادة جامعية', 'University Certificate Extraction', 60.0),
            ('استخراج قسيمة زواج', 'Marriage Certificate Extraction', 35.0),
            ('استخراج شهادة ميلاد', 'Birth Certificate Extraction', 20.0),
            ('استخراج شهادة وفاة', 'Death Certificate Extraction', 20.0),
            ('استخراج جواز سفر', 'Passport Extraction', 80.0),
            ('استخراج رخصة قيادة', 'Driving License Extraction', 30.0),
            ('استخراج شهادة عسكرية', 'Military Certificate Extraction', 40.0)
        ]
        
        for name_ar, name_en, price in procedure_types_data:
            existing = ProcedureType.query.filter_by(name_ar=name_ar).first()
            if not existing:
                procedure_type = ProcedureType(
                    name_ar=name_ar,
                    name_en=name_en,
                    price=price,
                    is_active=True
                )
                db.session.add(procedure_type)
        
        print("✓ Procedure types initialized")
        
        # Create zone pricing
        zone_pricing_data = [
            ('المنطقة الأولى', 'Zone 1', 2.5, 'kuwait_to_sudan'),
            ('المنطقة الثانية', 'Zone 2', 3.0, 'kuwait_to_sudan'),
            ('المنطقة الثالثة', 'Zone 3', 3.5, 'kuwait_to_sudan'),
            ('المنطقة الرابعة', 'Zone 4', 4.0, 'kuwait_to_sudan'),
            ('المنطقة الأولى', 'Zone 1', 2.8, 'sudan_to_kuwait'),
            ('المنطقة الثانية', 'Zone 2', 3.3, 'sudan_to_kuwait'),
            ('المنطقة الثالثة', 'Zone 3', 3.8, 'sudan_to_kuwait'),
            ('المنطقة الرابعة', 'Zone 4', 4.3, 'sudan_to_kuwait')
        ]
        
        for zone_name_ar, zone_name_en, price_per_kg, direction in zone_pricing_data:
            existing = ZonePricing.query.filter_by(
                zone_name_ar=zone_name_ar, 
                direction=direction
            ).first()
            if not existing:
                zone_pricing = ZonePricing(
                    zone_name_ar=zone_name_ar,
                    zone_name_en=zone_name_en,
                    price_per_kg=price_per_kg,
                    direction=direction,
                    is_active=True
                )
                db.session.add(zone_pricing)
        
        print("✓ Zone pricing initialized")
        
        # Create packaging types
        packaging_types_data = [
            ('صندوق صغير', 'Small Box', 2.0),
            ('صندوق متوسط', 'Medium Box', 3.0),
            ('صندوق كبير', 'Large Box', 5.0),
            ('ظرف', 'Envelope', 1.0),
            ('بلاستيك', 'Plastic Wrap', 1.5),
            ('بدون تغليف', 'No Packaging', 0.0)
        ]
        
        for name_ar, name_en, cost in packaging_types_data:
            existing = PackagingType.query.filter_by(name_ar=name_ar).first()
            if not existing:
                packaging_type = PackagingType(
                    name_ar=name_ar,
                    name_en=name_en,
                    cost=cost,
                    is_active=True
                )
                db.session.add(packaging_type)
        
        print("✓ Packaging types initialized")
        
        # Create global settings
        global_settings_data = [
            ('price_per_kg', 2.500),
            ('packaging_price', 2.000),
            ('waybill_price', 5.000),
            ('default_currency', 1),  # 1 for KWD
            ('tax_rate', 0.0),
            ('discount_rate', 0.0)
        ]
        
        for setting_key, setting_value in global_settings_data:
            existing = GlobalSettings.query.filter_by(setting_key=setting_key).first()
            if not existing:
                global_setting = GlobalSettings(
                    setting_key=setting_key,
                    setting_value=setting_value
                )
                db.session.add(global_setting)
        
        print("✓ Global settings initialized")
        
        # Create air shipping costs
        existing_air_costs = AirShippingCosts.query.first()
        if not existing_air_costs:
            air_costs = AirShippingCosts(
                price_per_kg=3.500,
                packaging_price=2.000,
                kuwait_transport_price=1.500,
                sudan_transport_price=2.000,
                clearance_price=5.000
            )
            db.session.add(air_costs)
            print("✓ Air shipping costs initialized")
        
        # Create document costs
        existing_doc_costs = DocumentCosts.query.first()
        if not existing_doc_costs:
            doc_costs = DocumentCosts(
                doc_authentication_foreign=50.0,
                doc_authentication_education=30.0,
                doc_criminal_record=25.0,
                doc_secondary_certificate=40.0,
                doc_university_certificate=60.0,
                doc_marriage_registered=35.0,
                doc_marriage_unregistered=45.0,
                doc_university_details=70.0
            )
            db.session.add(doc_costs)
            print("✓ Document costs initialized")
        
        # Commit all changes
        db.session.commit()
        print("✓ Database initialization completed successfully!")
        
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION SUMMARY")
        print("="*50)
        print(f"Admin users: {Admin.query.count()}")
        print(f"Shipment types: {ShipmentType.query.count()}")
        print(f"Document types: {DocumentType.query.count()}")
        print(f"Procedure types: {ProcedureType.query.count()}")
        print(f"Zone pricing: {ZonePricing.query.count()}")
        print(f"Packaging types: {PackagingType.query.count()}")
        print(f"Global settings: {GlobalSettings.query.count()}")
        print("="*50)
        print("Login credentials: admin / admin123")
        print("="*50)

if __name__ == '__main__':
    initialize_database()