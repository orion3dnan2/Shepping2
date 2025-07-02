from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSONB
import os
import json
import logging

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    permissions = db.Column(JSONB, nullable=True, default={})  # JSONB field for permissions (PostgreSQL optimized)
    is_super_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_permissions(self, permissions_dict):
        """Set user permissions as JSONB (PostgreSQL optimized)"""
        self.permissions = permissions_dict
    
    def get_permissions(self):
        """Get user permissions as dictionary"""
        return self.permissions if self.permissions else {}
    
    def has_permission(self, page):
        """Check if user has permission for a specific page"""
        if self.is_super_admin:
            return True
        permissions = self.get_permissions()
        return permissions.get(page, False)

    def __repr__(self):
        return f'<Admin {self.username}>'

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Sender details
    sender_name = db.Column(db.String(100), nullable=False)
    sender_phone = db.Column(db.String(50), nullable=False)
    sender_address = db.Column(db.String(200), nullable=True)
    sender_email = db.Column(db.String(100), nullable=True)
    
    # Receiver details
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(50), nullable=False)
    receiver_address = db.Column(db.String(200), nullable=True)
    receiver_email = db.Column(db.String(100), nullable=True)
    
    # Shipment details
    direction = db.Column(db.String(50), nullable=False, default='kuwait_to_sudan')
    package_type = db.Column(db.String(50), nullable=False, default='general')
    shipping_method = db.Column(db.String(20), nullable=True)  # جوي or بري (Air or Land shipping)
    package_contents = db.Column(db.String(200), nullable=True)
    document_type = db.Column(db.String(100), nullable=True)  # New field for document type
    weight = db.Column(db.Float, nullable=False)
    zone = db.Column(db.String(50), nullable=True)  # Zone for pricing (e.g., 'zone1', 'zone2', 'zone3')
    packaging = db.Column(db.String(50), nullable=True)  # Packaging type (e.g., 'box', 'envelope', 'none')
    has_packaging = db.Column(db.Boolean, nullable=False, default=False)  # Packaging checkbox
    has_policy = db.Column(db.Boolean, nullable=False, default=False)  # Policy checkbox
    has_comment = db.Column(db.Boolean, nullable=False, default=False)  # Comment checkbox
    waybill_price = db.Column(db.Float, nullable=False, default=0.0)  # Manual waybill price
    status = db.Column(db.String(50), nullable=False, default='created')
    price = db.Column(db.Float, nullable=False, default=0.0)  # سعر الشحن للعميل
    discount = db.Column(db.Float, nullable=False, default=0.0)  # خصم من السعر الإجمالي
    cost = db.Column(db.Float, nullable=False, default=0.0)  # تكلفة الشحنة الفعلية
    profit = db.Column(db.Float, nullable=False, default=0.0)  # ربح الشحنة (محسوب تلقائياً)
    paid_amount = db.Column(db.Float, nullable=False, default=0.0)  # Amount paid by customer
    remaining_amount = db.Column(db.Float, nullable=False, default=0.0)  # Remaining amount to be paid
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Location tracking fields
    sender_latitude = db.Column(db.Float, nullable=True)
    sender_longitude = db.Column(db.Float, nullable=True)
    receiver_latitude = db.Column(db.Float, nullable=True)
    receiver_longitude = db.Column(db.Float, nullable=True)
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)
    last_location_update = db.Column(db.DateTime, nullable=True)
    
    # Linked expenses for individual shipment P&L calculation
    linked_expenses = db.Column(db.Float, nullable=False, default=0.0)  # إجمالي المصروفات المرتبطة بالشحنة
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Shipment {self.tracking_number}>'
    
    def calculate_total_expenses(self):
        """Calculate total expenses linked to this shipment"""
        total = 0.0
        
        # Get expenses from FinancialTransaction table
        financial_expenses = FinancialTransaction.query.filter_by(
            transaction_type='expense', 
            shipment_id=self.id
        ).all()
        
        for expense in financial_expenses:
            total += float(expense.amount)
        
        # Get expenses from ExpenseGeneral table (office expenses linked to shipment)
        general_expenses = ExpenseGeneral.query.filter_by(shipment_id=self.id).all()
        for expense in general_expenses:
            total += float(expense.amount)
        
        # Get expenses from ExpenseDocuments table (document expenses linked to shipment)
        document_expenses = ExpenseDocuments.query.filter_by(shipment_id=self.id).all()
        for expense in document_expenses:
            total += float(expense.amount)
        
        return total
    
    def calculate_net_profit(self):
        """Calculate net profit for this shipment (Revenue - Expenses)"""
        revenue = float(self.price)  # Customer price
        expenses = self.calculate_total_expenses()
        return revenue - expenses

    def calculate_category_distributed_expenses(self):
        """Calculate distributed category expenses per shipment based on shipment type"""
        try:
            if self.package_type == 'document':
                # Get total document expenses and count of document shipments
                total_expenses = self.get_total_document_category_expenses()
                document_count = Shipment.query.filter_by(package_type='document').count()
                return total_expenses / document_count if document_count > 0 else 0.0
            else:
                # Get total general expenses and count of general shipments
                total_expenses = self.get_total_general_category_expenses()
                general_count = Shipment.query.filter(Shipment.package_type != 'document').count()
                return total_expenses / general_count if general_count > 0 else 0.0
        except Exception as e:
            logging.error(f'Error calculating distributed category expenses for shipment {self.id}: {str(e)}')
            return 0.0

    @staticmethod
    def get_total_document_category_expenses():
        """Get total expenses for all document shipments category"""
        try:
            # Get all document expenses from FinancialTransaction
            financial_expenses = FinancialTransaction.query.filter_by(
                transaction_type='expense',
                shipping_type='مستندات'
            ).all()
            
            # Get all document expenses from ExpenseDocuments
            document_expenses = ExpenseDocuments.query.all()
            
            total = 0.0
            for expense in financial_expenses:
                total += float(expense.amount) if expense.amount else 0.0
            for expense in document_expenses:
                total += float(expense.amount) if expense.amount else 0.0
                
            return total
        except Exception as e:
            logging.error(f'Error calculating total document category expenses: {str(e)}')
            return 0.0

    @staticmethod
    def get_total_general_category_expenses():
        """Get total expenses for all general shipments category"""
        try:
            # Get all general expenses from FinancialTransaction
            financial_expenses = FinancialTransaction.query.filter_by(
                transaction_type='expense',
                shipping_type='شحنات عامة'
            ).all()
            
            # Get all general expenses from ExpenseGeneral
            general_expenses = ExpenseGeneral.query.all()
            
            total = 0.0
            for expense in financial_expenses:
                total += float(expense.amount) if expense.amount else 0.0
            for expense in general_expenses:
                total += float(expense.amount) if expense.amount else 0.0
                
            return total
        except Exception as e:
            logging.error(f'Error calculating total general category expenses: {str(e)}')
            return 0.0

    def calculate_net_profit_with_category_expenses(self):
        """Calculate net profit using distributed category expenses"""
        revenue = float(self.price) if self.price else 0.0
        category_expenses = self.calculate_category_distributed_expenses()
        return revenue - category_expenses
    
    def update_linked_expenses(self):
        """Update the linked_expenses field with calculated total"""
        self.linked_expenses = self.calculate_total_expenses()
        db.session.commit()
        return self.linked_expenses

    @staticmethod
    def generate_tracking_number():
        """Generate a unique tracking number in format SHIP-YYYYMMDD-XXX"""
        from datetime import datetime
        
        # Get current date
        today = datetime.now()
        date_str = today.strftime("%Y%m%d")
        
        # Find the last shipment created today
        today_start = datetime(today.year, today.month, today.day)
        today_end = datetime(today.year, today.month, today.day, 23, 59, 59)
        
        last_shipment = Shipment.query.filter(
            Shipment.created_at >= today_start,
            Shipment.created_at <= today_end
        ).order_by(Shipment.id.desc()).first()
        
        # Calculate sequence number
        if last_shipment:
            # Extract the sequence number from the last tracking number
            last_sequence = int(last_shipment.tracking_number.split('-')[-1])
            sequence = last_sequence + 1
        else:
            sequence = 1
        
        # Format sequence number with leading zeros
        sequence_str = f"{sequence:03d}"
        
        return f"SHIP-{date_str}-{sequence_str}"
    
    @staticmethod
    def get_total_shipment_revenue(start_date=None, end_date=None):
        """Get total revenue from shipments (paid amounts) within date range"""
        query = Shipment.query
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        return sum([s.paid_amount for s in query.all()])
    
    @staticmethod
    def get_packaging_revenue(start_date=None, end_date=None):
        """Get total packaging revenue within date range"""
        query = Shipment.query.filter_by(has_packaging=True)
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        packaging_price = GlobalSettings.get_setting('packaging_price', 0.0)
        return len(query.all()) * packaging_price
    
    @staticmethod
    def get_policy_revenue(start_date=None, end_date=None):
        """Get total policy (waybill) revenue within date range"""
        query = Shipment.query.filter_by(has_policy=True)
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        return sum([s.waybill_price for s in query.all() if s.waybill_price])
    
    @staticmethod
    def get_general_shipments_revenue(start_date=None, end_date=None):
        """Get total revenue from general shipments (non-document) within date range"""
        query = Shipment.query.filter(Shipment.package_type != 'document')
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        return sum([s.paid_amount for s in query.all()])

    @staticmethod
    def get_documents_revenue(start_date=None, end_date=None):
        """Get total revenue from document shipments within date range"""
        query = Shipment.query.filter(Shipment.package_type == 'document')
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        return sum([s.paid_amount for s in query.all()])

    @staticmethod
    def get_shipment_counts(start_date=None, end_date=None):
        """Get shipment statistics within date range"""
        query = Shipment.query
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        
        shipments = query.all()
        total_count = len(shipments)
        paid_count = len([s for s in shipments if s.remaining_amount == 0])
        unpaid_count = len([s for s in shipments if s.remaining_amount > 0])
        
        return {
            'total': total_count,
            'paid': paid_count,
            'unpaid': unpaid_count
        }


class ShipmentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ShipmentType {self.name_ar}>'


class DocumentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<DocumentType {self.name_ar}>'


class ProcedureType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProcedureType {self.name_ar}>'


class ZonePricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zone_name_ar = db.Column(db.String(100), nullable=False)
    zone_name_en = db.Column(db.String(100), nullable=False)
    price_per_kg = db.Column(db.Float, nullable=False, default=0.0)
    direction = db.Column(db.String(50), nullable=False, default='kuwait_to_sudan')  # kuwait_to_sudan or sudan_to_kuwait
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ZonePricing {self.zone_name_ar}>'


class PackagingType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False, default=0.0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<PackagingType {self.name_ar}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    tracking_number = db.Column(db.String(20), nullable=True)
    shipment_type = db.Column(db.String(50), nullable=True)  # 'document' or other
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)

    def __repr__(self):
        return f'<Notification {self.title}>'


class GlobalSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Float, nullable=False, default=0.000)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<GlobalSettings {self.setting_key}: {self.setting_value}>'

    @staticmethod
    def get_setting(key, default=0.0):
        """Get a setting value by key"""
        setting = GlobalSettings.query.filter_by(setting_key=key).first()
        return setting.setting_value if setting else default

    @staticmethod
    def set_setting(key, value):
        """Set a setting value by key"""
        setting = GlobalSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = float(value)
            setting.updated_at = datetime.utcnow()
        else:
            setting = GlobalSettings(setting_key=key, setting_value=float(value))
            db.session.add(setting)
        db.session.commit()
        return setting


class OperationalCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)  # نوع التكلفة التشغيلية
    name = db.Column(db.String(200), nullable=False)  # اسم التكلفة
    amount = db.Column(db.Float, nullable=False)  # المبلغ
    cost_type = db.Column(db.String(50), nullable=False)  # monthly, per_shipment, per_kg
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)

    def __repr__(self):
        return f'<OperationalCost {self.name}>'

    @staticmethod
    def get_monthly_costs(start_date=None, end_date=None):
        """Get total monthly operational costs within date range"""
        query = OperationalCost.query.filter_by(cost_type='monthly', is_active=True)
        if start_date:
            query = query.filter(OperationalCost.created_at >= start_date)
        if end_date:
            query = query.filter(OperationalCost.created_at <= end_date)
        return sum([cost.amount for cost in query.all()])

    @staticmethod
    def get_costs_by_category(category, start_date=None, end_date=None):
        """Get operational costs by category within date range"""
        query = OperationalCost.query.filter_by(category=category, is_active=True)
        if start_date:
            query = query.filter(OperationalCost.created_at >= start_date)
        if end_date:
            query = query.filter(OperationalCost.created_at <= end_date)
        return sum([cost.amount for cost in query.all()])


class FinancialTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # 'expense' or 'revenue'
    revenue_type = db.Column(db.String(100), nullable=True)  # 'general_shipments' or 'documents' for revenues
    shipping_type = db.Column(db.String(100), nullable=True)  # 'شحن بري', 'شحن جوي', 'مستندات' for expenses
    category = db.Column(db.String(100), nullable=True)  # Category for filtering
    description = db.Column(db.Text, nullable=True)  # Additional notes
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Allows custom date
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    # Link to specific shipment for P&L analysis
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=True)
    
    def __repr__(self):
        return f'<FinancialTransaction {self.name}: {self.amount}>'
    
    @staticmethod
    def get_total_expenses(start_date=None, end_date=None):
        """Get total expenses within date range"""
        query = FinancialTransaction.query.filter_by(transaction_type='expense')
        if start_date:
            query = query.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(FinancialTransaction.transaction_date <= end_date)
        return sum([t.amount for t in query.all()])
    
    @staticmethod
    def get_total_revenues(start_date=None, end_date=None):
        """Get total manual revenues within date range"""
        query = FinancialTransaction.query.filter_by(transaction_type='revenue')
        if start_date:
            query = query.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(FinancialTransaction.transaction_date <= end_date)
        return sum([t.amount for t in query.all()])

    @staticmethod
    def get_revenues_by_type(revenue_type, start_date=None, end_date=None):
        """Get total revenues by type within date range"""
        query = FinancialTransaction.query.filter_by(
            transaction_type='revenue',
            revenue_type=revenue_type
        )
        if start_date:
            query = query.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(FinancialTransaction.transaction_date <= end_date)
        return sum([t.amount for t in query.all()])

    @staticmethod
    def get_expenses_by_shipping_type(shipping_type, start_date=None, end_date=None):
        """Get total expenses by shipping type within date range"""
        query = FinancialTransaction.query.filter_by(
            transaction_type='expense',
            shipping_type=shipping_type
        )
        if start_date:
            query = query.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(FinancialTransaction.transaction_date <= end_date)
        return sum([t.amount for t in query.all()])

    @staticmethod
    def get_expenses_by_shipping_type_list(shipping_type, start_date=None, end_date=None):
        """Get expense list by shipping type within date range"""
        query = FinancialTransaction.query.filter_by(
            transaction_type='expense',
            shipping_type=shipping_type
        )
        if start_date:
            query = query.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(FinancialTransaction.transaction_date <= end_date)
        return query.order_by(FinancialTransaction.transaction_date.desc()).all()


class AirShippingCosts(db.Model):
    """Air shipping specific cost configuration model"""
    id = db.Column(db.Integer, primary_key=True)
    price_per_kg = db.Column(db.Float, nullable=False, default=0.0)  # سعر الكيلو/طيران
    packaging_price = db.Column(db.Float, nullable=False, default=0.0)  # سعر التغليف
    kuwait_transport_price = db.Column(db.Float, nullable=False, default=0.0)  # سعر الترحيل في الكويت
    sudan_transport_price = db.Column(db.Float, nullable=False, default=0.0)  # سعر الترحيل في السودان
    clearance_price = db.Column(db.Float, nullable=False, default=0.0)  # سعر التخليص
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)

    def __repr__(self):
        return f'<AirShippingCosts {self.id}>'

    @staticmethod
    def get_current_costs():
        """Get the most recent air shipping costs configuration"""
        return AirShippingCosts.query.order_by(AirShippingCosts.updated_at.desc()).first()

    @staticmethod
    def get_total_air_shipping_cost_per_kg():
        """Calculate total cost per kg for air shipping including all components"""
        costs = AirShippingCosts.get_current_costs()
        if not costs:
            return 0.0
        return costs.price_per_kg + costs.packaging_price

    @staticmethod
    def get_total_processing_costs():
        """Get total processing costs (transport + clearance)"""
        costs = AirShippingCosts.get_current_costs()
        if not costs:
            return 0.0
        return costs.kuwait_transport_price + costs.sudan_transport_price + costs.clearance_price

    @staticmethod
    def create_or_update_costs(price_per_kg, packaging_price, kuwait_transport_price, 
                              sudan_transport_price, clearance_price, admin_id=None):
        """Create new cost configuration or update existing"""
        new_costs = AirShippingCosts(
            price_per_kg=price_per_kg,
            packaging_price=packaging_price,
            kuwait_transport_price=kuwait_transport_price,
            sudan_transport_price=sudan_transport_price,
            clearance_price=clearance_price,
            admin_id=admin_id
        )
        db.session.add(new_costs)
        db.session.commit()
        return new_costs


class DocumentCosts(db.Model):
    """Document processing costs configuration model"""
    __tablename__ = 'document_costs'
    
    id = db.Column(db.Integer, primary_key=True)
    doc_authentication_foreign = db.Column(db.Float, nullable=False, default=0.0)  # توثيق خارجية
    doc_authentication_education = db.Column(db.Float, nullable=False, default=0.0)  # توثيق تعليم عالي
    doc_criminal_record = db.Column(db.Float, nullable=False, default=0.0)  # أدلة جنائية / فيش
    doc_secondary_certificate = db.Column(db.Float, nullable=False, default=0.0)  # استخراج شهادة ثانوية
    doc_university_certificate = db.Column(db.Float, nullable=False, default=0.0)  # استخراج شهادة جامعية
    doc_marriage_registered = db.Column(db.Float, nullable=False, default=0.0)  # استخراج قسيمة زواج مدرجة
    doc_marriage_unregistered = db.Column(db.Float, nullable=False, default=0.0)  # استخراج قسيمة زواج غير مدرجة
    doc_university_details = db.Column(db.Float, nullable=False, default=0.0)  # استخراج شهادة جامعية تفاصيل
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)

    def __repr__(self):
        return f'<DocumentCosts {self.id}>'

    @staticmethod
    def get_current_costs():
        """Get the most recent document costs configuration"""
        return DocumentCosts.query.order_by(DocumentCosts.created_at.desc()).first()

    @staticmethod
    def create_or_update_costs(doc_authentication_foreign, doc_authentication_education, 
                              doc_criminal_record, doc_secondary_certificate, 
                              doc_university_certificate, doc_marriage_registered, 
                              doc_marriage_unregistered, doc_university_details, admin_id=None):
        """Create new document costs configuration"""
        new_costs = DocumentCosts(
            doc_authentication_foreign=doc_authentication_foreign,
            doc_authentication_education=doc_authentication_education,
            doc_criminal_record=doc_criminal_record,
            doc_secondary_certificate=doc_secondary_certificate,
            doc_university_certificate=doc_university_certificate,
            doc_marriage_registered=doc_marriage_registered,
            doc_marriage_unregistered=doc_marriage_unregistered,
            doc_university_details=doc_university_details,
            admin_id=admin_id
        )
        db.session.add(new_costs)
        db.session.commit()
        return new_costs



class ExpenseGeneral(db.Model):
    """Model for general expenses"""
    __tablename__ = 'expenses_general'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 3), nullable=False)
    notes = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Link to specific shipment for P&L analysis
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=True)
    
    def __repr__(self):
        return f'<ExpenseGeneral {self.name}: {self.amount}>'


class ExpenseDocuments(db.Model):
    """Model for document shipping expenses"""
    __tablename__ = 'expenses_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 3), nullable=False)
    notes = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Link to specific shipment for P&L analysis
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=True)
    
    def __repr__(self):
        return f'<ExpenseDocuments {self.name}: {self.amount}>'
