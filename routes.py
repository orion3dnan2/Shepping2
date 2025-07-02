from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import app, db
from models import Admin, Shipment, ShipmentType, DocumentType, Notification, ZonePricing, PackagingType, GlobalSettings, FinancialTransaction, OperationalCost, ExpenseGeneral, ExpenseDocuments
import logging
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from translations import get_text
import json
from functools import wraps

# Helper function to get document type Arabic name
def get_document_type_arabic(document_type_en):
    """Get Arabic name for document type from English name"""
    if not document_type_en:
        return "مستندات"
    
    try:
        doc_type = DocumentType.query.filter_by(name_en=document_type_en).first()
        if doc_type:
            return doc_type.name_ar
    except:
        pass
    
    return document_type_en  # Fallback to English name if not found

# Make get_text and helper functions available in all templates
@app.context_processor
def inject_get_text():
    def get_permission_arabic(permission_key):
        """Get Arabic name for permission key"""
        permission_map = {
            'home': 'الرئيسية',
            'shipments': 'الشحنات',
            'tracking': 'التتبع',
            'reports': 'التقارير',
            'expenses': 'المصروفات',
            'add_shipment': 'إضافة شحنة جديدة'
        }
        return permission_map.get(permission_key, permission_key)
    
    def get_shipment_status_display(status):
        """Get Arabic display name and CSS class for shipment status"""
        status_map = {
            'created': {'name': 'تم الإنشاء', 'class': 'status-created'},
            'packaged': {'name': 'تم التغليف', 'class': 'status-packaged'},
            'dispatching': {'name': 'جاري الإرسال', 'class': 'status-dispatching'},
            'shipped': {'name': 'تم الإرسال', 'class': 'status-shipped'},
            'in_transit': {'name': 'في الطريق', 'class': 'status-in-transit'},
            'received': {'name': 'تم الاستلام', 'class': 'status-received'},
            'delivered': {'name': 'تم التسليم', 'class': 'status-delivered'},
            'cancelled': {'name': 'ملغي', 'class': 'status-cancelled'},
            # Legacy status support
            'processing': {'name': 'قيد المعالجة', 'class': 'status-processing'},
            'pending': {'name': 'في الانتظار', 'class': 'status-pending'}
        }
        return status_map.get(status, {'name': 'تم الإنشاء', 'class': 'status-created'})
    
    return {'get_text': get_text, 'get_document_type_arabic': get_document_type_arabic, 'get_permission_arabic': get_permission_arabic, 'get_shipment_status_display': get_shipment_status_display}

def permission_required(page):
    """Decorator to check if user has permission for a specific page"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            if not current_user.has_permission(page):
                flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('يرجى إدخال اسم المستخدم وكلمة المرور', 'error')
            return render_template('login.html')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            next_page = request.args.get('next')
            flash(f'مرحباً {username}! تم تسجيل الدخول بنجاح', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    from datetime import datetime, timedelta
    from sqlalchemy import extract, and_
    
    # Dashboard statistics
    total_shipments = Shipment.query.count()
    delivered_count = Shipment.query.filter_by(status='delivered').count()
    in_transit_count = Shipment.query.filter(Shipment.status.in_(['in_transit', 'shipped', 'dispatching'])).count()
    pending_count = Shipment.query.filter(Shipment.status.in_(['created', 'packaged'])).count()
    
    # Calculate total revenue from delivered shipments including all fees
    delivered_shipments = Shipment.query.filter_by(status='delivered').all()
    total_revenue = 0
    for shipment in delivered_shipments:
        # Base price
        revenue = shipment.price
        
        # Add packaging cost if applicable
        if shipment.has_packaging:
            packaging_price = GlobalSettings.get_setting('packaging_price', 0)
            revenue += packaging_price
        
        # Add waybill price if applicable
        if shipment.has_policy:
            revenue += shipment.waybill_price
        
        # Add comment price if applicable
        if shipment.has_comment:
            comment_price = GlobalSettings.get_setting('comment_price', 0)
            revenue += comment_price
            
        total_revenue += revenue
    
    # Monthly statistics (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Monthly shipments count
    monthly_shipments = Shipment.query.filter(
        and_(
            extract('month', Shipment.created_at) == current_month,
            extract('year', Shipment.created_at) == current_year
        )
    ).count()
    
    # Monthly delivered shipments count
    monthly_delivered = Shipment.query.filter(
        and_(
            extract('month', Shipment.created_at) == current_month,
            extract('year', Shipment.created_at) == current_year,
            Shipment.status == 'delivered'
        )
    ).count()
    
    # Monthly revenue from delivered shipments
    monthly_delivered_shipments = Shipment.query.filter(
        and_(
            extract('month', Shipment.created_at) == current_month,
            extract('year', Shipment.created_at) == current_year,
            Shipment.status == 'delivered'
        )
    ).all()
    
    monthly_revenue = 0
    for shipment in monthly_delivered_shipments:
        # Base price
        revenue = shipment.price
        
        # Add packaging cost if applicable
        if shipment.has_packaging:
            packaging_price = GlobalSettings.get_setting('packaging_price', 0)
            revenue += packaging_price
        
        # Add waybill price if applicable
        if shipment.has_policy:
            revenue += shipment.waybill_price
        
        # Add comment price if applicable
        if shipment.has_comment:
            comment_price = GlobalSettings.get_setting('comment_price', 0)
            revenue += comment_price
            
        monthly_revenue += revenue
    
    # Monthly completion rate
    monthly_completion_rate = 0
    if monthly_shipments > 0:
        monthly_completion_rate = (monthly_delivered / monthly_shipments) * 100
    
    # Get recent shipments (last 5 for dashboard)
    recent_shipments = Shipment.query.order_by(Shipment.created_at.desc()).limit(5).all()
    
    # Current month name for display
    import calendar
    current_month_name = calendar.month_name[current_month]
    
    return render_template('dashboard.html',
                         total_shipments=total_shipments,
                         delivered_count=delivered_count,
                         in_transit_count=in_transit_count,
                         pending_count=pending_count,
                         total_revenue=total_revenue,
                         monthly_shipments=monthly_shipments,
                         monthly_delivered=monthly_delivered,
                         monthly_revenue=monthly_revenue,
                         monthly_completion_rate=monthly_completion_rate,
                         current_month=current_month,
                         current_month_name=current_month_name,
                         current_year=current_year,
                         recent_shipments=recent_shipments)

@app.route('/api/dashboard_stats')
@login_required
def get_dashboard_stats():
    """API endpoint for real-time dashboard statistics"""
    from datetime import datetime
    from sqlalchemy import extract, and_
    
    # Dashboard statistics
    total_shipments = Shipment.query.count()
    delivered_count = Shipment.query.filter_by(status='delivered').count()
    in_transit_count = Shipment.query.filter(Shipment.status.in_(['in_transit', 'shipped', 'dispatching'])).count()
    pending_count = Shipment.query.filter(Shipment.status.in_(['created', 'packaged'])).count()
    
    # Calculate total revenue from delivered shipments including all fees
    delivered_shipments = Shipment.query.filter_by(status='delivered').all()
    total_revenue = 0
    for shipment in delivered_shipments:
        # Base price
        revenue = shipment.price
        
        # Add packaging cost if applicable
        if shipment.has_packaging:
            packaging_price = GlobalSettings.get_setting('packaging_price', 0)
            revenue += packaging_price
        
        # Add waybill price if applicable
        if shipment.has_policy:
            revenue += shipment.waybill_price
        
        # Add comment price if applicable
        if shipment.has_comment:
            comment_price = GlobalSettings.get_setting('comment_price', 0)
            revenue += comment_price
            
        total_revenue += revenue
    
    # Monthly statistics (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Monthly shipments count
    monthly_shipments = Shipment.query.filter(
        and_(
            extract('month', Shipment.created_at) == current_month,
            extract('year', Shipment.created_at) == current_year
        )
    ).count()
    
    # Monthly delivered shipments count
    monthly_delivered = Shipment.query.filter(
        and_(
            extract('month', Shipment.created_at) == current_month,
            extract('year', Shipment.created_at) == current_year,
            Shipment.status == 'delivered'
        )
    ).count()
    
    # Monthly revenue from delivered shipments
    monthly_delivered_shipments = Shipment.query.filter(
        and_(
            extract('month', Shipment.created_at) == current_month,
            extract('year', Shipment.created_at) == current_year,
            Shipment.status == 'delivered'
        )
    ).all()
    
    monthly_revenue = 0
    for shipment in monthly_delivered_shipments:
        # Base price
        revenue = shipment.price
        
        # Add packaging cost if applicable
        if shipment.has_packaging:
            packaging_price = GlobalSettings.get_setting('packaging_price', 0)
            revenue += packaging_price
        
        # Add waybill price if applicable
        if shipment.has_policy:
            revenue += shipment.waybill_price
        
        # Add comment price if applicable
        if shipment.has_comment:
            comment_price = GlobalSettings.get_setting('comment_price', 0)
            revenue += comment_price
            
        monthly_revenue += revenue
    
    # Monthly completion rate
    monthly_completion_rate = 0
    if monthly_shipments > 0:
        monthly_completion_rate = (monthly_delivered / monthly_shipments) * 100
    
    # Format currency properly
    def format_currency(amount):
        if amount > 0:
            return f"{amount:,.2f} د.ك"
        else:
            return "لا توجد بيانات بعد"
    
    return jsonify({
        'total_shipments': total_shipments,
        'delivered_count': delivered_count,
        'in_transit_count': in_transit_count,
        'pending_count': pending_count,
        'total_revenue': format_currency(total_revenue),
        'total_revenue_raw': total_revenue,
        'monthly_shipments': monthly_shipments,
        'monthly_delivered': monthly_delivered,
        'monthly_revenue': format_currency(monthly_revenue),
        'monthly_revenue_raw': monthly_revenue,
        'monthly_completion_rate': monthly_completion_rate,
        'monthly_shipments_text': f"{monthly_shipments} شحنة ({monthly_delivered} مسلمة)" if monthly_shipments > 0 else "لا توجد شحنات",
        'completion_rate_text': f"معدل الإكمال: {monthly_completion_rate:.1f}%" if monthly_completion_rate > 0 else ""
    })



@app.route('/add_shipment', methods=['GET', 'POST'])
@login_required
@permission_required('add_shipment')
def add_shipment():
    # Get dynamic types from database for form display
    shipment_types = ShipmentType.query.filter_by(is_active=True).order_by(ShipmentType.name_ar).all()
    document_types = DocumentType.query.filter_by(is_active=True).order_by(DocumentType.name_ar).all()
    zone_pricings = ZonePricing.query.filter_by(is_active=True).order_by(ZonePricing.zone_name_ar).all()
    packaging_types = PackagingType.query.filter_by(is_active=True).order_by(PackagingType.name_ar).all()
    
    # Get pricing settings from GlobalSettings
    packaging_price = GlobalSettings.get_setting('packaging_price', 0.0)
    comment_price = GlobalSettings.get_setting('comment_price', 0.0)
    if request.method == 'POST':
        try:
            # Debug: Log all form data
            app.logger.debug(f"Form data received: {dict(request.form)}")
            
            # Get form data with defaults
            sender_name = request.form.get('sender_name', 'غير محدد').strip()
            sender_phone = request.form.get('sender_phone', '').strip()
            sender_address = request.form.get('sender_address', '').strip()
            sender_email = request.form.get('sender_email', '').strip()
            
            receiver_name = request.form.get('receiver_name', 'غير محدد').strip()
            receiver_phone = request.form.get('receiver_phone', '').strip()
            receiver_address = request.form.get('receiver_address', '').strip()
            receiver_email = request.form.get('receiver_email', '').strip()
            
            direction = request.form.get('direction', 'kuwait_to_sudan').strip()
            package_type = request.form.get('package_type', 'general').strip()
            shipping_method = request.form.get('shipping_method', '').strip()
            package_contents = request.form.get('package_contents', '').strip()
            action_required = request.form.get('action_required', '').strip()
            document_type = request.form.get('document_type', '').strip()
            zone = request.form.get('zone', '').strip()
            
            # Handle packaging checkbox
            has_packaging = request.form.get('has_packaging') == '1'
            packaging = ''  # Keep for backward compatibility
            
            # Handle policy checkbox
            has_policy = request.form.get('has_policy') == '1'
            
            # Handle comment checkbox
            has_comment = request.form.get('has_comment') == '1'
            
            # Handle manual waybill price
            waybill_price = 0.0
            if has_policy:
                waybill_price_str = request.form.get('waybill_price', '0').strip()
                try:
                    waybill_price = float(waybill_price_str) if waybill_price_str else 0.0
                except ValueError:
                    app.logger.debug(f"Invalid waybill_price: '{waybill_price_str}', defaulting to 0.0")
                    waybill_price = 0.0
            
            # Handle numeric fields with proper validation
            weight_str = request.form.get('weight', '1.0').strip()
            price_str = request.form.get('total_price', '0.0').strip()
            discount_str = request.form.get('discount', '0.0').strip()
            paid_amount_str = request.form.get('amount_paid', '0.0').strip()
            
            confirmed = request.form.get('confirmed') == 'on'
            notes = request.form.get('notes', '').strip()
            status = request.form.get('status', 'created').strip()
            
            app.logger.debug(f"Processed form data - weight: '{weight_str}', price: '{price_str}', discount: '{discount_str}', paid_amount: '{paid_amount_str}'")
            
            # Initialize default values
            weight = 1.0
            price = 0.0
            discount = 0.0
            
            # Validate required fields (all fields are now optional per requirements)
            errors = []
            
            # Process weight and price with comprehensive error handling
            if package_type == 'document':
                # For documents: document_type required, weight/contents/price not required
                if document_type:
                    # For documents, store action_required in package_contents field
                    if action_required:
                        package_contents = action_required
                    # Get price from document type
                    try:
                        doc_type = DocumentType.query.filter_by(name_en=document_type).first()
                        if doc_type:
                            price = doc_type.price
                        app.logger.debug(f"Document type price: {price}")
                    except Exception as e:
                        app.logger.error(f"Error fetching document type price: {e}")
                        price = 0.0
                weight = 0.0  # Documents don't have weight
            else:
                # For non-documents: process weight and price
                try:
                    weight = float(weight_str) if weight_str else 1.0
                    if weight <= 0:
                        weight = 1.0
                    app.logger.debug(f"Processed weight: {weight}")
                except ValueError:
                    app.logger.debug(f"Invalid weight '{weight_str}', defaulting to 1.0")
                    weight = 1.0
                
                try:
                    price = float(price_str) if price_str else 0.0
                    if price < 0:
                        price = 0.0
                    app.logger.debug(f"Processed price: {price}")
                except ValueError:
                    app.logger.debug(f"Invalid price '{price_str}', defaulting to 0.0")
                    price = 0.0
                
                # Process discount with error handling
                try:
                    discount = float(discount_str) if discount_str else 0.0
                    if discount < 0:
                        discount = 0.0
                    app.logger.debug(f"Processed discount: {discount}")
                except ValueError:
                    app.logger.debug(f"Invalid discount '{discount_str}', defaulting to 0.0")
                    discount = 0.0
            
            # Process paid amount with error handling
            paid_amount = 0.0
            try:
                paid_amount = float(paid_amount_str) if paid_amount_str else 0.0
                if paid_amount < 0:
                    paid_amount = 0.0
                app.logger.debug(f"Processed paid_amount: {paid_amount}")
            except ValueError:
                app.logger.debug(f"Invalid paid_amount '{paid_amount_str}', defaulting to 0.0")
                paid_amount = 0.0
            
            # Show errors if any exist
            if errors:
                for error in errors:
                    flash(error, 'error')
                app.logger.debug(f"Validation errors: {errors}")
                return redirect(url_for('add_shipment'))
            
            # Generate tracking number
            tracking_number = Shipment.generate_tracking_number()
            
            # Create new shipment - package_type and document_type already extracted above
            document_type = document_type if package_type == 'document' else None
            
            # Get cost and calculate profit with error handling
            cost_str = request.form.get('cost', '0').strip()
            try:
                cost = float(cost_str) if cost_str else 0.0
            except ValueError:
                cost = 0.0
                app.logger.debug(f"Invalid cost value: '{cost_str}', defaulting to 0.0")
            
            profit = price - cost
            
            # Calculate remaining amount
            remaining_amount = price - paid_amount
            
            # Debug: Log all variables before database insertion
            app.logger.debug(f"Creating shipment with values:")
            app.logger.debug(f"  tracking_number: {tracking_number}")
            app.logger.debug(f"  sender_name: {sender_name}")
            app.logger.debug(f"  weight: {weight} (type: {type(weight)})")
            app.logger.debug(f"  price: {price} (type: {type(price)})")
            app.logger.debug(f"  discount: {discount} (type: {type(discount)})")
            app.logger.debug(f"  cost: {cost} (type: {type(cost)})")
            app.logger.debug(f"  profit: {profit} (type: {type(profit)})")
            app.logger.debug(f"  paid_amount: {paid_amount} (type: {type(paid_amount)})")
            app.logger.debug(f"  remaining_amount: {remaining_amount} (type: {type(remaining_amount)})")
            app.logger.debug(f"  waybill_price: {waybill_price} (type: {type(waybill_price)})")
            
            shipment = Shipment(
                tracking_number=tracking_number,
                sender_name=sender_name,
                sender_phone=sender_phone,
                sender_address=sender_address,
                sender_email=sender_email,
                receiver_name=receiver_name,
                receiver_phone=receiver_phone,
                receiver_address=receiver_address,
                receiver_email=receiver_email,
                direction=direction,
                package_type=package_type,
                shipping_method=shipping_method,
                package_contents=package_contents,
                document_type=document_type,
                zone=zone,
                packaging=packaging,
                has_packaging=has_packaging,
                has_policy=has_policy,
                has_comment=has_comment,
                waybill_price=waybill_price,
                weight=weight,
                price=price,
                discount=discount,
                cost=cost,
                profit=profit,
                paid_amount=paid_amount,
                remaining_amount=remaining_amount,
                confirmed=confirmed,
                notes=notes,
                status=status
            )
            
            # Save to database
            db.session.add(shipment)
            db.session.commit()
            
            # Create notification for new shipment
            notification = Notification(
                title='شحنة جديدة',
                message=f'تم إنشاء شحنة جديدة برقم تتبع: {tracking_number}',
                tracking_number=tracking_number,
                shipment_type=package_type,
                admin_id=current_user.id
            )
            db.session.add(notification)
            db.session.commit()
            
            flash(f'تم إنشاء الشحنة بنجاح! رقم التتبع: {tracking_number}', 'success')
            logging.info(f'New shipment created: {tracking_number}')
            
            # Trigger revenue update for Financial Center real-time sync
            session['revenue_updated'] = True
            session['last_shipment_added'] = tracking_number
            
            return redirect(url_for('track_search'))
            
        except Exception as e:
            db.session.rollback()
            # Log comprehensive error details for debugging
            import traceback
            error_details = traceback.format_exc()
            app.logger.error(f"Error creating shipment: {str(e)}")
            app.logger.error(f"Full traceback: {error_details}")
            app.logger.debug(f"Form data that caused error: {dict(request.form)}")
            
            # Show detailed error message to user based on error type
            if "could not convert string to float" in str(e):
                flash('خطأ في تحويل البيانات الرقمية. تأكد من إدخال أرقام صحيحة في حقول الوزن والسعر والمبلغ المدفوع.', 'error')
            elif "IntegrityError" in str(e):
                flash('خطأ في قاعدة البيانات. قد يكون رقم التتبع مكرر أو هناك قيود أخرى.', 'error')
            elif "ValidationError" in str(e):
                flash('خطأ في التحقق من صحة البيانات. تأكد من ملء جميع الحقول المطلوبة بشكل صحيح.', 'error')
            elif "OperationalError" in str(e):
                flash('خطأ في الاتصال بقاعدة البيانات. يرجى المحاولة مرة أخرى.', 'error')
            else:
                flash(f'حدث خطأ أثناء إنشاء الشحنة: {str(e)}', 'error')
        
        return redirect(url_for('add_shipment'))
    
    # Get price per kg from session
    price_per_kg = session.get('price_per_kg', 0.000)
    
    # Get additional pricing from GlobalSettings
    packaging_price = GlobalSettings.get_setting('packaging_price', 0.000)
    
    # Convert zone_pricings to dict for JSON serialization
    zone_pricings_dict = [
        {
            'id': zp.id,
            'zone_name_ar': zp.zone_name_ar,
            'zone_name_en': zp.zone_name_en,
            'price_per_kg': float(zp.price_per_kg),
            'direction': zp.direction
        } for zp in zone_pricings
    ]
    
    return render_template('add_shipment.html', 
                         shipment_types=shipment_types, 
                         document_types=document_types,
                         zone_pricings=zone_pricings_dict,
                         packaging_types=packaging_types,
                         price_per_kg=price_per_kg,
                         packaging_price=packaging_price,
                         comment_price=comment_price)

# Removed duplicate update_status function - using the new one below

# Removed senders and receivers routes as requested

@app.route('/financial_center', methods=['GET', 'POST'])
@app.route('/financial-center', methods=['GET', 'POST'])
@login_required
@permission_required('expenses')
def financial_center():
    """Financial Center with comprehensive accounting system"""
    from datetime import datetime, timedelta
    
    # Get date filters from request
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    
    # Parse dates
    start_date = None
    end_date = None
    
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)  # End of day
    except ValueError:
        flash('تنسيق التاريخ غير صحيح', 'error')
        start_date = end_date = None
    
    # Default to current month if no dates provided
    if not start_date and not end_date:
        today = datetime.now()
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now()
    
    if request.method == 'POST':
        # Detect if this is an AJAX request (check for fetch or XMLHttpRequest)
        is_ajax = (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 
                  'application/json' in request.headers.get('Accept', '') or
                  request.args.get('ajax') == '1')
        
        try:
            # Check if this is an operational cost
            if request.form.get('transaction_type') == 'operational_cost':
                # Handle operational cost
                category = request.form.get('category', '').strip()
                name = request.form.get('name', '').strip()
                amount_str = request.form.get('amount', '').strip()
                cost_type = request.form.get('cost_type', 'monthly')
                
                if not category or not name or not amount_str:
                    flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                    return redirect(url_for('financial_center'))
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        flash('المبلغ يجب أن يكون أكبر من صفر', 'error')
                        return redirect(url_for('financial_center'))
                except ValueError:
                    flash('المبلغ يجب أن يكون رقماً صحيحاً', 'error')
                    return redirect(url_for('financial_center'))
                
                # Use category as name since name field was removed
                category_names = {
                    'office_rent': 'إيجار المكتب',
                    'storage_rent': 'إيجار التخزين',
                    'salaries': 'رواتب الموظفين',
                    'international_shipping': 'الشحن الدولي',
                    'packaging': 'التغليف',
                    'local_delivery_kw': 'التوصيل - الكويت',
                    'local_delivery_sd': 'التوصيل - السودان',
                    'customs_clearance': 'التخليص الجمركي',
                    'other': 'مصاريف أخرى'
                }
                
                operational_cost = OperationalCost(
                    category=category,
                    name=category_names.get(category, category),
                    amount=amount,
                    cost_type=cost_type,
                    admin_id=current_user.id
                )
                
                db.session.add(operational_cost)
                db.session.commit()
                flash('تم إضافة التكلفة التشغيلية بنجاح', 'success')
                return redirect(url_for('financial_center'))
            
            # Handle regular financial transactions
            name = request.form.get('name', '').strip()
            amount_str = request.form.get('amount', '').strip()
            transaction_type = request.form.get('transaction_type', '')
            category = request.form.get('category', '').strip()
            description = request.form.get('description', '').strip()
            transaction_date_str = request.form.get('transaction_date', '').strip()
            shipment_id = request.form.get('shipment_id') or None
            

            
            # Validate inputs
            if not name:
                error_msg = 'يرجى إدخال اسم المعاملة'
                if is_ajax:
                    return jsonify({'success': False, 'message': error_msg})
                flash(error_msg, 'error')
                return redirect(url_for('financial_center'))
            
            if not amount_str:
                error_msg = 'يرجى إدخال المبلغ'
                if is_ajax:
                    return jsonify({'success': False, 'message': error_msg})
                flash(error_msg, 'error')
                return redirect(url_for('financial_center'))
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    error_msg = 'المبلغ يجب أن يكون أكبر من صفر'
                    if is_ajax:
                        return jsonify({'success': False, 'message': error_msg})
                    flash(error_msg, 'error')
                    return redirect(url_for('financial_center'))
            except ValueError:
                error_msg = 'المبلغ يجب أن يكون رقماً صحيحاً'
                if is_ajax:
                    return jsonify({'success': False, 'message': error_msg})
                flash(error_msg, 'error')
                return redirect(url_for('financial_center'))
            
            if transaction_type not in ['expense', 'revenue']:
                error_msg = 'نوع المعاملة غير صحيح'
                if is_ajax:
                    return jsonify({'success': False, 'message': error_msg})
                flash(error_msg, 'error')
                return redirect(url_for('financial_center'))
            
            # Parse transaction date
            transaction_date = datetime.now()
            if transaction_date_str:
                try:
                    transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d')
                except ValueError:
                    error_msg = 'تنسيق التاريخ غير صحيح'
                    if is_ajax:
                        return jsonify({'success': False, 'message': error_msg})
                    flash(error_msg, 'error')
                    return redirect(url_for('financial_center'))
            
            # Get revenue type for revenue transactions
            revenue_type = request.form.get('revenue_type') if transaction_type == 'revenue' else None
            
            # Get shipping type for expenses
            shipping_type = request.form.get('shipping_type') if transaction_type == 'expense' else None
            
            # Create new financial transaction
            transaction = FinancialTransaction(
                name=name,
                amount=amount,
                transaction_type=transaction_type,
                revenue_type=revenue_type,
                shipping_type=shipping_type,
                category=category or None,
                description=description or None,
                transaction_date=transaction_date,
                admin_id=current_user.id,
                shipment_id=int(shipment_id) if shipment_id else None
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            success_message = f'تم إضافة {"المصروف" if transaction_type == "expense" else "الإيراد"} بنجاح'
            
            # Return JSON for AJAX requests
            if is_ajax:
                return jsonify({'success': True, 'message': success_message})
            
            flash(success_message, 'success')
            
        except Exception as e:
            db.session.rollback()
            error_message = f'حدث خطأ أثناء إضافة المعاملة: {str(e)}'
            logging.error(f'Error adding financial transaction: {str(e)}')
            
            # Return JSON for AJAX requests
            if is_ajax:
                return jsonify({'success': False, 'message': error_message})
            
            flash('حدث خطأ أثناء إضافة المعاملة', 'error')
            return redirect(url_for('financial_center'))
        
        return redirect(url_for('financial_center'))
    
    # Get filtered transactions
    expense_query = FinancialTransaction.query.filter_by(transaction_type='expense')
    revenue_query = FinancialTransaction.query.filter_by(transaction_type='revenue')
    
    if start_date:
        expense_query = expense_query.filter(FinancialTransaction.transaction_date >= start_date)
        revenue_query = revenue_query.filter(FinancialTransaction.transaction_date >= start_date)
    
    if end_date:
        expense_query = expense_query.filter(FinancialTransaction.transaction_date <= end_date)
        revenue_query = revenue_query.filter(FinancialTransaction.transaction_date <= end_date)
    
    expenses = expense_query.order_by(FinancialTransaction.transaction_date.desc()).all()
    revenues = revenue_query.order_by(FinancialTransaction.transaction_date.desc()).all()
    
    # Calculate comprehensive accounting report
    # 1. Manual revenues and expenses
    total_manual_expenses = FinancialTransaction.get_total_expenses(start_date, end_date)
    total_manual_revenues = FinancialTransaction.get_total_revenues(start_date, end_date)
    
    # 2. Calculate automatic revenues from shipments database
    general_shipments_revenue = Shipment.get_general_shipments_revenue(start_date, end_date)
    documents_revenue = Shipment.get_documents_revenue(start_date, end_date)
    
    # 3. Manual "other" revenues only
    other_revenues_manual = FinancialTransaction.get_revenues_by_type('other', start_date, end_date)
    
    # 4. Total shipment revenue from database
    total_shipment_revenue = general_shipments_revenue + documents_revenue
    total_packaging_revenue = Shipment.get_packaging_revenue(start_date, end_date)
    total_policy_revenue = Shipment.get_policy_revenue(start_date, end_date)
    
    # 5. Total revenues including other manual revenues
    total_revenues = other_revenues_manual + total_shipment_revenue + total_packaging_revenue + total_policy_revenue
    
    # 5. Net profit/loss
    net_profit = total_revenues - total_manual_expenses
    
    # 6. Shipment statistics
    shipment_stats = Shipment.get_shipment_counts(start_date, end_date)
    
    # Prepare accounting report data
    accounting_report = {
        'total_revenues': total_revenues,
        'manual_revenues': total_manual_revenues,
        'shipment_revenue': total_shipment_revenue,
        'packaging_revenue': total_packaging_revenue,
        'policy_revenue': total_policy_revenue,
        'total_expenses': total_manual_expenses,
        'net_profit': net_profit,
        'shipment_stats': shipment_stats,
        'start_date': start_date,
        'end_date': end_date
    }
    
    # Get operational costs
    operational_costs_query = OperationalCost.query.filter_by(is_active=True)
    if start_date:
        operational_costs_query = operational_costs_query.filter(OperationalCost.created_at >= start_date)
    if end_date:
        operational_costs_query = operational_costs_query.filter(OperationalCost.created_at <= end_date)
    
    operational_costs = operational_costs_query.order_by(OperationalCost.created_at.desc()).all()
    
    # Calculate total operational costs
    total_operational_costs = sum(cost.amount for cost in operational_costs)
    
    return render_template('financial_center.html', 
                         expenses=expenses, 
                         revenues=revenues,
                         operational_costs=operational_costs,
                         total_operational_costs=total_operational_costs,
                         total_shipment_revenue=total_shipment_revenue,
                         total_manual_revenues=total_manual_revenues,
                         general_shipments_revenue=general_shipments_revenue,
                         documents_revenue=documents_revenue,
                         other_revenues_manual=other_revenues_manual,
                         total_expenses=total_manual_expenses,
                         packaging_revenue=total_packaging_revenue,
                         policy_revenue=total_policy_revenue,
                         total_all_revenues=total_revenues,
                         net_profit=net_profit,
                         shipment_count=shipment_stats['total'],
                         start_date_str=start_date_str,
                         end_date_str=end_date_str)


@app.route('/api/revenue_totals')
@login_required
@permission_required('expenses')
def get_revenue_totals():
    """API endpoint for real-time revenue totals by type"""
    try:
        # Calculate automatic revenues from shipments database
        general_shipments_revenue = Shipment.get_general_shipments_revenue()
        documents_revenue = Shipment.get_documents_revenue()
        
        # Manual "other" revenues only
        other_revenues_manual = FinancialTransaction.get_revenues_by_type('other')
        
        # Total revenues
        total_revenues = general_shipments_revenue + documents_revenue + other_revenues_manual
        
        return jsonify({
            'general_shipments': general_shipments_revenue,
            'documents': documents_revenue,
            'other': other_revenues_manual,
            'total': total_revenues
        })
    except Exception as e:
        logging.error(f'Error getting revenue totals: {str(e)}')
        return jsonify({'error': 'Failed to get revenue totals'}), 500

@app.route('/api/expense_invoice')
@login_required
@permission_required('expenses')
def get_expense_invoice():
    """API endpoint for real-time expense invoice"""
    try:
        expenses = FinancialTransaction.query.filter_by(transaction_type='expense').order_by(FinancialTransaction.created_at.desc()).all()
        total_expenses = sum([expense.amount for expense in expenses])
        
        expense_items = [{'name': expense.name, 'amount': expense.amount} for expense in expenses]
        
        return jsonify({
            'expenses': expense_items,
            'total': total_expenses
        })
    except Exception as e:
        logging.error(f'Error getting expense invoice: {str(e)}')
        return jsonify({'error': 'Failed to get expense invoice'}), 500

@app.route('/delete_financial_transaction/<int:transaction_id>', methods=['POST'])
@login_required
@permission_required('expenses')
def delete_financial_transaction(transaction_id):
    """Delete a financial transaction"""
    try:
        transaction = FinancialTransaction.query.get(transaction_id)
        
        if not transaction:
            return jsonify({'success': False, 'message': 'المعاملة غير موجودة'})
        
        transaction_type = "مصروف" if transaction.transaction_type == 'expense' else "إيراد"
        
        db.session.delete(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'تم حذف ال{transaction_type} بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting financial transaction: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء حذف المعاملة'})


@app.route('/edit_financial_transaction/<int:transaction_id>', methods=['POST'])
@login_required
@permission_required('expenses')
def edit_financial_transaction(transaction_id):
    """Edit a financial transaction"""
    try:
        transaction = FinancialTransaction.query.get(transaction_id)
        
        if not transaction:
            return jsonify({'success': False, 'message': 'المعاملة غير موجودة'})
        
        # Update transaction fields
        transaction.name = request.form.get('name', transaction.name)
        
        # Handle amount conversion with error handling
        try:
            amount_str = request.form.get('amount', '0')
            transaction.amount = float(amount_str) if amount_str else transaction.amount
        except ValueError:
            return jsonify({'success': False, 'message': 'قيمة المبلغ غير صحيحة'})
        
        transaction.category = request.form.get('category', transaction.category)
        transaction.description = request.form.get('description', transaction.description)
        
        # Handle date conversion
        date_str = request.form.get('transaction_date')
        if date_str:
            try:
                from datetime import datetime
                transaction.transaction_date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({'success': False, 'message': 'تاريخ غير صحيح'})
        
        transaction.admin_id = current_user.id
        
        db.session.commit()
        
        transaction_type = "مصروف" if transaction.transaction_type == 'expense' else "إيراد"
        
        return jsonify({
            'success': True, 
            'message': f'تم تحديث ال{transaction_type} بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error editing financial transaction: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء تحديث المعاملة'})


@app.route('/delete_operational_cost/<int:cost_id>', methods=['POST'])
@login_required
@permission_required('expenses')
def delete_operational_cost(cost_id):
    """Delete an operational cost"""
    try:
        cost = OperationalCost.query.get(cost_id)
        
        if not cost:
            return jsonify({'success': False, 'message': 'التكلفة التشغيلية غير موجودة'})
        
        db.session.delete(cost)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'تم حذف التكلفة التشغيلية بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting operational cost: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء حذف التكلفة التشغيلية'})


# Legacy expenses route redirect
@app.route('/expenses')
@login_required
@permission_required('expenses')
def expenses():
    """Redirect old expenses route to financial center"""
    return redirect(url_for('financial_center'))


def calculate_expenses_old():
    from datetime import datetime
    from sqlalchemy import func
    
    # Default expense rates (could be stored in database in a real system)
    default_rates = {
        'flight_rate': 0.55,  # per kg
        'packaging_rate': 1.50,  # per kg
        'kuwait_transport': 3.00,  # per kg
        'sudan_transport': 3.00,  # per kg
        'clearance': 3.00,  # per kg
        'other_expenses': 1.00  # per kg
    }
    
    # Handle rate updates
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_rates':
            # In a real system, you would save these to database
            flash('تم تحديث أسعار المصروفات بنجاح', 'success')
        elif action == 'reset_rates':
            flash('تم إعادة تعيين الأسعار إلى القيم الافتراضية', 'info')
    
    # Calculate statistics from actual shipment data
    today = datetime.now().date()
    total_shipments = Shipment.query.count()
    total_revenue = db.session.query(func.sum(Shipment.price)).scalar() or 0
    avg_cost = total_revenue / total_shipments if total_shipments > 0 else 0
    
    # Get current rates (from form if posted, otherwise defaults)
    current_rates = {}
    for key in default_rates:
        current_rates[key] = float(request.form.get(key, default_rates[key]))
    
    return render_template('expenses.html',
                         today=today,
                         total_shipments=total_shipments,
                         total_revenue=total_revenue,
                         avg_cost=avg_cost,
                         rates=current_rates)



@app.route('/track')
def track_search():
    tracking_number = request.args.get('tracking_number', '').strip()
    error_message = None
    
    if tracking_number:
        # Search for shipment
        shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
        if shipment:
            # Conditional routing based on shipment type
            if shipment.package_type == 'document':
                return redirect(url_for('track_document', tracking_number=tracking_number))
            else:
                return redirect(url_for('track_shipment', tracking_number=tracking_number))
        else:
            error_message = f'لم يتم العثور على شحنة بالرقم: {tracking_number}'
    
    # Get some example tracking numbers for display
    example_shipments = Shipment.query.order_by(Shipment.created_at.desc()).limit(3).all()
    
    return render_template('track_search.html', 
                         tracking_number=tracking_number,
                         error_message=error_message,
                         example_shipments=example_shipments)

@app.route('/track/<tracking_number>')
@login_required
def track_shipment(tracking_number):
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first_or_404()
    
    # Redirect to document tracking if it's a document shipment
    if shipment.package_type == 'document':
        return redirect(url_for('track_document', tracking_number=tracking_number))
    
    # Create timeline based on shipment status and dates
    timeline = [
        {
            'title': 'تم إنشاء الشحنة',
            'description': f'تم إنشاء الشحنة برقم التتبع {tracking_number}',
            'timestamp': shipment.created_at,
            'icon': 'fas fa-plus-circle',
            'status': 'completed',
            'color': 'success'
        }
    ]
    
    if shipment.status in ['in_transit', 'delivered']:
        timeline.append({
            'title': 'تم الإرسال',
            'description': 'تم إرسال الشحنة من نقطة الانطلاق',
            'timestamp': shipment.created_at,  # Would be actual send date in real system
            'icon': 'fas fa-shipping-fast',
            'status': 'completed',
            'color': 'info'
        })
        
        timeline.append({
            'title': 'في الطريق',
            'description': 'الشحنة في طريقها إلى الوجهة',
            'timestamp': None,
            'icon': 'fas fa-truck',
            'status': 'completed' if shipment.status == 'delivered' else 'current',
            'color': 'warning'
        })
    else:
        timeline.append({
            'title': 'لم يتم الإرسال بعد',
            'description': 'في انتظار إرسال الشحنة',
            'timestamp': None,
            'icon': 'fas fa-clock',
            'status': 'pending',
            'color': 'secondary'
        })
    
    if shipment.status == 'delivered':
        timeline.append({
            'title': 'تم التسليم',
            'description': 'تم تسليم الشحنة بنجاح للمستلم',
            'timestamp': shipment.created_at,  # Would be actual delivery date in real system
            'icon': 'fas fa-check-circle',
            'status': 'completed',
            'color': 'success'
        })
    else:
        timeline.append({
            'title': 'لم يتم التسليم بعد',
            'description': 'في انتظار وصول الشحنة للمستلم',
            'timestamp': None,
            'icon': 'fas fa-map-marker-alt',
            'status': 'pending',
            'color': 'secondary'
        })
    
    return render_template('track_shipment.html', shipment=shipment, timeline=timeline)

@app.route('/update-status/<int:shipment_id>', methods=['POST'])
@login_required
def update_status(shipment_id):
    """Update shipment status and sync with database"""
    shipment = Shipment.query.get_or_404(shipment_id)
    
    new_status = request.form.get('new_status')
    if new_status:
        # Define allowed status values for tracking stages
        allowed_statuses = ['created', 'packaged', 'dispatching', 'shipped', 'in_transit', 'received', 'delivered', 'cancelled']
        
        if new_status in allowed_statuses:
            old_status = shipment.status
            shipment.status = new_status
            db.session.commit()
            
            # Use the unified status display function
            status_display_fn = inject_get_text()['get_shipment_status_display']
            old_status_info = status_display_fn(old_status)
            new_status_info = status_display_fn(new_status)
            
            flash(f'تم تحديث حالة الشحنة من "{old_status_info["name"]}" إلى "{new_status_info["name"]}"', 'success')
            logging.info(f'Shipment status updated: {shipment.tracking_number} -> {old_status} to {new_status}')
        else:
            flash('حالة غير صحيحة', 'error')
    else:
        flash('يرجى اختيار حالة صحيحة', 'error')
    
    return redirect(url_for('track_shipment', tracking_number=shipment.tracking_number))

@app.route('/track-document/<tracking_number>')
@login_required
def track_document(tracking_number):
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first_or_404()
    
    if shipment.package_type != 'document':
        flash('هذه الشحنة ليست من نوع المستندات', 'warning')
        return redirect(url_for('track_shipment', tracking_number=tracking_number))
    
    return render_template('track_document.html', shipment=shipment, get_document_status_text=get_document_status_text)

@app.route('/update-document-status/<int:shipment_id>', methods=['POST'])
@login_required
def update_document_status(shipment_id):
    shipment = Shipment.query.get_or_404(shipment_id)
    
    if shipment.package_type != 'document':
        flash('هذه الشحنة ليست من نوع المستندات', 'error')
        return redirect(url_for('track_shipment', tracking_number=shipment.tracking_number))
    
    new_status = request.form.get('new_status')
    if new_status:
        old_status = shipment.status
        shipment.status = new_status
        db.session.commit()
        flash(f'{get_text("document_status_updated")}: {get_document_status_text(new_status)}', 'success')
        logging.info(f'Document status updated: {shipment.tracking_number} -> {old_status} to {new_status}')
    else:
        flash('يرجى اختيار حالة صحيحة', 'error')
    
    return redirect(url_for('track_document', tracking_number=shipment.tracking_number))

def get_document_status_text(status):
    """Get Arabic text for document status"""
    status_map = {
        'created': 'تم الإنشاء',
        'document_received': 'تم استلام المستند',
        'document_sent': 'تم إرسال المستند',
        'document_arrived': 'تم استلام المستند',
        'authentication_in_progress': 'جاري التوثيق',
        'authentication_completed': 'تم التوثيق',
        'sending_after_auth': 'جاري الإرسال بعد التوثيق',
        'received_after_auth': 'تم الاستلام بعد التوثيق',
        'delivered': 'تم التسليم'
    }
    return status_map.get(status, 'حالة غير معروفة')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# User Management Routes
@app.route('/user_management')
@login_required
def user_management():
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('index'))
    
    users = Admin.query.all()
    return render_template('user_management.html', users=users)

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لإضافة مستخدمين', 'error')
        return redirect(url_for('index'))
    
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        permissions_list = request.form.getlist('permissions')
        
        # Validation
        if not username or not password:
            flash('اسم المستخدم وكلمة المرور مطلوبان', 'error')
            return redirect(url_for('settings') + '#users')
        
        # Check if username already exists
        if Admin.query.filter_by(username=username).first():
            flash('اسم المستخدم موجود بالفعل', 'error')
            return redirect(url_for('settings') + '#users')
        
        # Create permissions dictionary - use lowercase keys to match form values
        permissions = {
            'home': 'home' in permissions_list,
            'shipments': 'shipments' in permissions_list,
            'tracking': 'tracking' in permissions_list,
            'reports': 'reports' in permissions_list,
            'expenses': 'expenses' in permissions_list,
            'add_shipment': 'add_shipment' in permissions_list,
            'settings': 'settings' in permissions_list,
        }
        
        # Create new user
        new_user = Admin(username=username, is_super_admin=False)
        new_user.set_password(password)
        new_user.set_permissions(permissions)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'تم إنشاء المستخدم "{username}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء إنشاء المستخدم', 'error')
    
    return redirect(url_for('settings') + '#users')

@app.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لتحرير المستخدمين', 'error')
        return redirect(url_for('index'))
    
    try:
        user = Admin.query.get_or_404(user_id)
        
        # Allow super admin to be edited by other super admins
        if user.is_super_admin and not current_user.is_super_admin:
            flash('لا يمكن تحرير المدير العام إلا من قبل مدير عام آخر', 'error')
            return redirect(url_for('settings') + '#users')
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        permissions_list = request.form.getlist('permissions')
        is_super_admin = 'is_super_admin' in request.form
        
        # Validation
        if not username:
            flash('اسم المستخدم مطلوب', 'error')
            return redirect(url_for('settings') + '#users')
        
        # Check if username already exists (excluding current user)
        existing_user = Admin.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            flash('اسم المستخدم موجود بالفعل', 'error')
            return redirect(url_for('settings') + '#users')
        
        # Update user
        user.username = username
        if password:  # Only update password if provided
            user.set_password(password)
        
        # Update super admin status if current user is super admin
        if current_user.is_super_admin:
            user.is_super_admin = is_super_admin
        
        # Update permissions - use lowercase keys to match form values
        permissions = {
            'home': 'home' in permissions_list,
            'shipments': 'shipments' in permissions_list,
            'tracking': 'tracking' in permissions_list,
            'reports': 'reports' in permissions_list,
            'expenses': 'expenses' in permissions_list,
            'add_shipment': 'add_shipment' in permissions_list,
            'settings': 'settings' in permissions_list,
        }
        user.set_permissions(permissions)
        
        db.session.commit()
        flash(f'تم تحديث المستخدم "{username}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء تحديث المستخدم', 'error')
    
    return redirect(url_for('settings') + '#users')




# Settings Page Route
@app.route('/settings')
@login_required
@permission_required('settings')
def settings():
    # Get all types and users data
    shipment_types = ShipmentType.query.filter_by(is_active=True).order_by(ShipmentType.created_at.desc()).all()
    document_types = DocumentType.query.filter_by(is_active=True).order_by(DocumentType.created_at.desc()).all()
    users = Admin.query.all()
    
    # Calculate total pricing
    total_pricing = sum([st.price for st in shipment_types]) + sum([dt.price for dt in document_types])
    
    # Get price per kg from session
    price_per_kg = session.get('price_per_kg', 0.000)
    
    # Get additional pricing from GlobalSettings
    packaging_price = GlobalSettings.get_setting('packaging_price', 0.000)
    waybill_price = GlobalSettings.get_setting('waybill_price', 0.000)
    
    return render_template('settings.html', 
                         shipment_types=shipment_types,
                         document_types=document_types,
                         price_per_kg=price_per_kg,
                         packaging_price=packaging_price,
                         waybill_price=waybill_price,
                         users=users,
                         total_pricing=total_pricing)

# Shipments Routes
@app.route('/shipments')
@login_required
@permission_required('shipments')
def shipments():
    # Get all shipments
    all_shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    
    # Separate document shipments from regular shipments
    regular_shipments = [s for s in all_shipments if s.package_type != 'document']
    document_shipments = [s for s in all_shipments if s.package_type == 'document']
    
    # Get unpaid shipments (where remaining amount > 0)
    unpaid_shipments = [s for s in all_shipments if (s.remaining_amount if s.remaining_amount is not None else 0.0) > 0]
    
    return render_template('shipments.html',
                         regular_shipments=regular_shipments,
                         document_shipments=document_shipments,
                         unpaid_shipments=unpaid_shipments)

# Manage Types Routes - Redirect to Settings
@app.route('/manage_types')
@login_required
def manage_types():
    return redirect(url_for('settings') + '#types')


@app.route('/add_shipment_type', methods=['POST'])
@login_required
def add_shipment_type():
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لإضافة أنواع الشحنات', 'error')
        return redirect(url_for('index'))
    
    try:
        name_ar = request.form.get('name_ar', '').strip()
        name_en = request.form.get('name_en', '').strip() or name_ar
        
        if not name_ar:
            flash('يرجى إدخال الاسم بالعربية', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Check if type already exists
        existing_type = ShipmentType.query.filter(
            (ShipmentType.name_ar == name_ar) | (ShipmentType.name_en == name_en)
        ).first()
        
        if existing_type:
            flash('نوع الشحنة موجود بالفعل', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Create new shipment type
        new_type = ShipmentType(name_ar=name_ar, name_en=name_en)
        db.session.add(new_type)
        db.session.commit()
        
        flash(f'تم إضافة نوع الشحنة "{name_ar}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء إضافة نوع الشحنة', 'error')
    
    return redirect(url_for('settings') + '#types')


@app.route('/add_document_type', methods=['POST'])
@login_required
def add_document_type():
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لإضافة أنواع الوثائق', 'error')
        return redirect(url_for('index'))
    
    try:
        name_ar = request.form.get('name_ar', '').strip()
        name_en = request.form.get('name_en', '').strip() or name_ar
        
        if not name_ar:
            flash('يرجى إدخال الاسم بالعربية', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Check if type already exists
        existing_type = DocumentType.query.filter(
            (DocumentType.name_ar == name_ar) | (DocumentType.name_en == name_en)
        ).first()
        
        if existing_type:
            flash('نوع الوثيقة موجود بالفعل', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Create new document type
        new_type = DocumentType(name_ar=name_ar, name_en=name_en)
        db.session.add(new_type)
        db.session.commit()
        
        flash(f'تم إضافة نوع الوثيقة "{name_ar}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء إضافة نوع الوثيقة', 'error')
    
    return redirect(url_for('settings') + '#types')


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('settings')
def delete_user(user_id):
    """Delete a user with proper error handling"""
    try:
        if not current_user.is_super_admin:
            return jsonify({'success': False, 'message': 'ليس لديك صلاحية لحذف المستخدمين'})
        
        user = Admin.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'المستخدم غير موجود'})
        
        # Prevent deleting the last super admin
        if user.is_super_admin:
            super_admin_count = Admin.query.filter_by(is_super_admin=True).count()
            if super_admin_count <= 1:
                return jsonify({'success': False, 'message': 'لا يمكن حذف آخر مدير عام في النظام'})
        
        # Prevent self-deletion
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'لا يمكنك حذف حسابك الشخصي'})
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'تم حذف المستخدم {username} بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting user: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء حذف المستخدم'})


@app.route('/api/shipping_expenses/<shipping_type>')
@login_required
@permission_required('expenses')
def get_shipping_expenses(shipping_type):
    """Get expenses for a specific shipping type"""
    try:
        # Get date filters from request
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        
        # Parse dates
        start_date = None
        end_date = None
        
        try:
            if start_date_str:
                from datetime import datetime
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            start_date = end_date = None
        
        # Handle consolidated "شحنات عامة" category
        if shipping_type == 'شحنات عامة':
            # Get expenses from both land and air shipping
            land_expenses = FinancialTransaction.get_expenses_by_shipping_type_list('شحن بري', start_date, end_date)
            air_expenses = FinancialTransaction.get_expenses_by_shipping_type_list('شحن جوي', start_date, end_date)
            general_expenses = FinancialTransaction.get_expenses_by_shipping_type_list('شحنات عامة', start_date, end_date)
            
            # Combine all expenses
            expenses = list(land_expenses) + list(air_expenses) + list(general_expenses)
            
            # Calculate total amount
            land_total = FinancialTransaction.get_expenses_by_shipping_type('شحن بري', start_date, end_date)
            air_total = FinancialTransaction.get_expenses_by_shipping_type('شحن جوي', start_date, end_date)
            general_total = FinancialTransaction.get_expenses_by_shipping_type('شحنات عامة', start_date, end_date)
            total_amount = land_total + air_total + general_total
        else:
            # Get expenses by specific shipping type
            expenses = FinancialTransaction.get_expenses_by_shipping_type_list(shipping_type, start_date, end_date)
            total_amount = FinancialTransaction.get_expenses_by_shipping_type(shipping_type, start_date, end_date)
        
        # Format expenses for response
        expense_list = []
        for expense in expenses:
            expense_list.append({
                'id': expense.id,
                'name': expense.name,
                'amount': expense.amount,
                'category': expense.category or '-',
                'transaction_date': expense.transaction_date.strftime('%Y-%m-%d'),
                'description': expense.description or '-'
            })
        
        return jsonify({
            'success': True,
            'expenses': expense_list,
            'total_amount': total_amount,
            'shipping_type': shipping_type,
            'count': len(expenses)
        })
        
    except Exception as e:
        logging.error(f'Error getting shipping expenses: {str(e)}')
        return jsonify({'success': False, 'error': 'خطأ في تحميل المصروفات'})


@app.route('/api/shipping_revenue/<shipping_method>')
@login_required
@permission_required('expenses')
def get_shipping_revenue(shipping_method):
    """Get shipment revenues for a specific shipping method (جوي or بري)"""
    try:
        # Get date filters from request
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        
        # Parse dates
        start_date = None
        end_date = None
        
        try:
            if start_date_str:
                from datetime import datetime
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            start_date = end_date = None
        
        # Get shipments by shipping method (exclude documents)
        query = Shipment.query.filter(
            Shipment.package_type != 'document',
            Shipment.shipping_method == shipping_method
        )
        
        if start_date:
            query = query.filter(Shipment.created_at >= start_date)
        if end_date:
            query = query.filter(Shipment.created_at <= end_date)
        
        shipments = query.order_by(Shipment.created_at.desc()).all()
        total_revenue = sum([s.paid_amount for s in shipments])
        
        # Format shipments for response
        shipment_list = []
        for shipment in shipments:
            shipment_list.append({
                'tracking_number': shipment.tracking_number,
                'sender_name': shipment.sender_name,
                'receiver_name': shipment.receiver_name,
                'price': shipment.price,
                'paid_amount': shipment.paid_amount,
                'created_at': shipment.created_at.strftime('%Y-%m-%d')
            })
        
        return jsonify({
            'success': True,
            'shipments': shipment_list,
            'total_revenue': total_revenue,
            'shipping_method': shipping_method,
            'count': len(shipments)
        })
        
    except Exception as e:
        logging.error(f'Error getting shipping revenue: {str(e)}')
        return jsonify({'success': False, 'error': 'خطأ في تحميل إيرادات الشحن'})


@app.route('/api/revenue_category/<category>')
@login_required
@permission_required('expenses')
def get_revenue_category(category):
    """Get revenues for a specific category (general_shipments or documents)"""
    try:
        # Get date filters from request
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        
        # Parse dates
        start_date = None
        end_date = None
        
        try:
            if start_date_str:
                from datetime import datetime
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            start_date = end_date = None
        
        # Get revenues by category
        query = FinancialTransaction.query.filter_by(
            transaction_type='revenue',
            revenue_type=category
        )
        if start_date:
            query = query.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(FinancialTransaction.transaction_date <= end_date)
        
        revenues = query.order_by(FinancialTransaction.transaction_date.desc()).all()
        
        # Group by shipping type for general_shipments
        if category == 'general_shipments':
            land_revenues = [r for r in revenues if r.shipping_type == 'شحن بري']
            air_revenues = [r for r in revenues if r.shipping_type == 'شحن جوي']
            
            land_total = sum([r.amount for r in land_revenues])
            air_total = sum([r.amount for r in air_revenues])
            
            # Format response for both shipping types
            land_list = []
            for revenue in land_revenues:
                land_list.append({
                    'id': revenue.id,
                    'name': revenue.name,
                    'amount': revenue.amount,
                    'transaction_date': revenue.transaction_date.strftime('%Y-%m-%d'),
                    'description': revenue.description or '-'
                })
            
            air_list = []
            for revenue in air_revenues:
                air_list.append({
                    'id': revenue.id,
                    'name': revenue.name,
                    'amount': revenue.amount,
                    'transaction_date': revenue.transaction_date.strftime('%Y-%m-%d'),
                    'description': revenue.description or '-'
                })
            
            return jsonify({
                'success': True,
                'category': category,
                'land_shipping': {
                    'revenues': land_list,
                    'total_amount': land_total,
                    'count': len(land_revenues)
                },
                'air_shipping': {
                    'revenues': air_list,
                    'total_amount': air_total,
                    'count': len(air_revenues)
                },
                'total_amount': land_total + air_total
            })
        else:
            # For documents category
            total_amount = sum([r.amount for r in revenues])
            
            revenue_list = []
            for revenue in revenues:
                revenue_list.append({
                    'id': revenue.id,
                    'name': revenue.name,
                    'amount': revenue.amount,
                    'transaction_date': revenue.transaction_date.strftime('%Y-%m-%d'),
                    'description': revenue.description or '-'
                })
            
            return jsonify({
                'success': True,
                'category': category,
                'revenues': revenue_list,
                'total_amount': total_amount,
                'count': len(revenues)
            })
        
    except Exception as e:
        logging.error(f'Error getting revenue category: {str(e)}')
        return jsonify({'success': False, 'error': 'خطأ في تحميل الإيرادات'})


@app.route('/api/financial_report')
@login_required
@permission_required('expenses')
def get_financial_report():
    """Generate comprehensive financial report for specified period"""
    try:
        from datetime import datetime, timedelta
        
        report_type = request.args.get('type', 'monthly')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Calculate date range based on report type if not provided
        if not start_date_str or not end_date_str:
            end_date = datetime.now()
            if report_type == 'weekly':
                start_date = end_date - timedelta(days=7)
            elif report_type == 'monthly':
                start_date = end_date - timedelta(days=30)
            elif report_type == 'yearly':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        end_date = end_date.replace(hour=23, minute=59, second=59)
        
        # 1. Get all shipments in the period
        total_shipments = Shipment.query.filter(
            Shipment.created_at >= start_date,
            Shipment.created_at <= end_date
        ).all()
        
        # Categorize shipments
        general_shipments = [s for s in total_shipments if s.package_type != 'document']
        document_shipments = [s for s in total_shipments if s.package_type == 'document']
        
        # Further categorize by shipping method
        air_shipments = [s for s in general_shipments if s.shipping_method == 'جوي']
        land_shipments = [s for s in general_shipments if s.shipping_method == 'بري']
        
        # Status categories
        completed_shipments = [s for s in total_shipments if s.status in ['delivered', 'received']]
        
        # 2. Calculate revenues from shipments database
        air_shipping_revenue = sum([float(s.paid_amount or 0) for s in air_shipments])
        land_shipping_revenue = sum([float(s.paid_amount or 0) for s in land_shipments])
        document_revenue = sum([float(s.paid_amount or 0) for s in document_shipments])
        
        general_revenue = air_shipping_revenue + land_shipping_revenue
        
        # 3. Get manual revenues (other revenues)
        other_revenues = FinancialTransaction.query.filter(
            FinancialTransaction.transaction_type == 'revenue',
            FinancialTransaction.transaction_date >= start_date,
            FinancialTransaction.transaction_date <= end_date
        ).all()
        other_revenue_total = sum([float(r.amount or 0) for r in other_revenues])
        
        total_revenue = general_revenue + document_revenue + other_revenue_total
        
        # 4. Calculate expenses
        all_expenses = FinancialTransaction.query.filter(
            FinancialTransaction.transaction_type == 'expense',
            FinancialTransaction.transaction_date >= start_date,
            FinancialTransaction.transaction_date <= end_date
        ).all()
        
        general_expenses_total = sum([float(e.amount or 0) for e in all_expenses if e.shipping_type in ['شحنات عامة', 'شحن بري', 'شحن جوي']])
        documents_expenses_total = sum([float(e.amount or 0) for e in all_expenses if e.shipping_type == 'مستندات'])
        manual_expenses_total = general_expenses_total + documents_expenses_total
        
        # Operational costs
        operational_costs = 0.0
        try:
            op_costs = OperationalCost.query.filter(
                OperationalCost.created_at >= start_date,
                OperationalCost.created_at <= end_date,
                OperationalCost.is_active == True
            ).all()
            operational_costs = sum([float(c.amount or 0) for c in op_costs])
        except:
            operational_costs = 0.0
        
        total_expenses = manual_expenses_total + operational_costs
        
        # 5. Calculate profit/loss with enhanced breakdown
        net_profit = total_revenue - total_expenses
        
        # Enhanced profit calculation with proper expense allocation
        land_expenses = sum([float(e.amount or 0) for e in all_expenses if e.shipping_type in ['شحنات عامة', 'شحن بري']]) * 0.6
        air_expenses = sum([float(e.amount or 0) for e in all_expenses if e.shipping_type in ['شحنات عامة', 'شحن جوي']]) * 0.4
        documents_expenses = documents_expenses_total
        
        land_profit = land_shipping_revenue - land_expenses
        air_profit = air_shipping_revenue - air_expenses
        documents_profit = document_revenue - documents_expenses
        
        # Calculate operational costs allocation
        land_operational_costs = operational_costs * 0.4  # 40% for land
        air_operational_costs = operational_costs * 0.3   # 30% for air
        documents_operational_costs = operational_costs * 0.3  # 30% for documents
        
        # 6. Cost analysis (admin only)
        cost_stats = {}
        if current_user.has_permission('expenses'):
            total_costs = sum([float(s.cost or 0) for s in total_shipments])
            total_profits = sum([float(s.profit or 0) for s in total_shipments])
            average_cost = total_costs / len(total_shipments) if total_shipments else 0
            profit_margin = (total_profits / total_revenue * 100) if total_revenue > 0 else 0
            
            cost_stats = {
                'total_costs': round(total_costs, 3),
                'total_profits': round(total_profits, 3),
                'average_cost': round(average_cost, 3),
                'profit_margin': round(profit_margin, 2)
            }
        
        # Prepare response
        response_data = {
            'success': True,
            'report_type': report_type,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            },
            'shipment_stats': {
                'general_count': len(general_shipments),
                'document_count': len(document_shipments),
                'completed_count': len(completed_shipments),
                'incomplete_count': len(total_shipments) - len(completed_shipments),
                'air_shipments_count': len(air_shipments),
                'land_shipments_count': len(land_shipments),
                'total_count': len(total_shipments)
            },
            'revenue_stats': {
                'general_revenue': round(general_revenue, 3),
                'document_revenue': round(document_revenue, 3),
                'air_shipping_revenue': round(air_shipping_revenue, 3),
                'land_shipping_revenue': round(land_shipping_revenue, 3),
                'other_revenue': round(other_revenue_total, 3),
                'total_revenue': round(total_revenue, 3)
            },
            'expense_stats': {
                'manual_expenses': round(manual_expenses_total, 3),
                'general_expenses': round(general_expenses_total, 3),
                'documents_expenses': round(documents_expenses_total, 3),
                'operational_costs': round(operational_costs, 3),
                'total_expenses': round(total_expenses, 3)
            },
            'profit_loss': {
                'total_revenue': round(total_revenue, 3),
                'total_expenses': round(total_expenses, 3),
                'net_profit': round(net_profit, 3),
                'land_revenue': round(land_shipping_revenue, 3),
                'land_expenses': round(land_expenses, 3),
                'land_operational_costs': round(land_operational_costs, 3),
                'land_net_profit': round(land_profit - land_operational_costs, 3),
                'land_shipments_count': len(land_shipments),
                'air_revenue': round(air_shipping_revenue, 3),
                'air_expenses': round(air_expenses, 3),
                'air_operational_costs': round(air_operational_costs, 3),
                'air_net_profit': round(air_profit - air_operational_costs, 3),
                'air_shipments_count': len(air_shipments),
                'documents_revenue': round(document_revenue, 3),
                'documents_expenses': round(documents_expenses, 3),
                'documents_operational_costs': round(documents_operational_costs, 3),
                'documents_net_profit': round(documents_profit - documents_operational_costs, 3),
                'documents_shipments_count': len(document_shipments)
            }
        }
        
        if cost_stats:
            response_data['cost_stats'] = cost_stats
        
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f'Error generating financial report: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'حدث خطأ في إنشاء التقرير: {str(e)}'})


@app.route('/edit_shipment_type/<int:type_id>', methods=['POST'])
@login_required
def edit_shipment_type(type_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لتعديل أنواع الشحنات', 'error')
        return redirect(url_for('index'))
    
    try:
        shipment_type = ShipmentType.query.get_or_404(type_id)
        
        name_ar = request.form.get('name_ar', '').strip()
        name_en = request.form.get('name_en', '').strip()
        price = request.form.get('price', '').strip()
        is_active = 'is_active' in request.form
        
        if not name_ar or not name_en:
            flash('يرجى إدخال الاسم بالعربية والإنجليزية', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Validate price
        try:
            price = float(price) if price else 0.0
            if price < 0:
                flash('السعر يجب أن يكون أكبر من أو يساوي صفر', 'error')
                return redirect(url_for('settings') + '#types')
        except ValueError:
            flash('السعر يجب أن يكون رقماً صحيحاً', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Check if type already exists (excluding current one)
        existing_type = ShipmentType.query.filter(
            ShipmentType.id != type_id,
            (ShipmentType.name_ar == name_ar) | (ShipmentType.name_en == name_en)
        ).first()
        
        if existing_type:
            flash('نوع الشحنة موجود بالفعل', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Update shipment type
        shipment_type.name_ar = name_ar
        shipment_type.name_en = name_en
        shipment_type.price = price
        shipment_type.is_active = is_active
        db.session.commit()
        
        flash(f'تم تحديث نوع الشحنة "{name_ar}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء تحديث نوع الشحنة', 'error')
    
    return redirect(url_for('settings') + '#types')


@app.route('/edit_document_type/<int:type_id>', methods=['POST'])
@login_required
def edit_document_type(type_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لتعديل أنواع الوثائق', 'error')
        return redirect(url_for('index'))
    
    try:
        document_type = DocumentType.query.get_or_404(type_id)
        
        name_ar = request.form.get('name_ar', '').strip()
        name_en = request.form.get('name_en', '').strip()
        price = request.form.get('price', '').strip()
        is_active = 'is_active' in request.form
        
        if not name_ar or not name_en:
            flash('يرجى إدخال الاسم بالعربية والإنجليزية', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Validate price
        try:
            price = float(price) if price else 0.0
            if price < 0:
                flash('السعر يجب أن يكون أكبر من أو يساوي صفر', 'error')
                return redirect(url_for('settings') + '#types')
        except ValueError:
            flash('السعر يجب أن يكون رقماً صحيحاً', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Check if type already exists (excluding current one)
        existing_type = DocumentType.query.filter(
            DocumentType.id != type_id,
            (DocumentType.name_ar == name_ar) | (DocumentType.name_en == name_en)
        ).first()
        
        if existing_type:
            flash('نوع الوثيقة موجود بالفعل', 'error')
            return redirect(url_for('settings') + '#types')
        
        # Update document type
        document_type.name_ar = name_ar
        document_type.name_en = name_en
        document_type.price = price
        document_type.is_active = is_active
        db.session.commit()
        
        flash(f'تم تحديث نوع الوثيقة "{name_ar}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء تحديث نوع الوثيقة', 'error')
    
    return redirect(url_for('settings') + '#types')


@app.route('/update_air_shipping_costs', methods=['POST'])
@login_required
@permission_required('expenses')
def update_air_shipping_costs():
    """Update air shipping cost configuration"""
    try:
        # Extract form data
        price_per_kg = float(request.form.get('price_per_kg', 0))
        packaging_price = float(request.form.get('packaging_price', 0))
        kuwait_transport_price = float(request.form.get('kuwait_transport_price', 0))
        sudan_transport_price = float(request.form.get('sudan_transport_price', 0))
        clearance_price = float(request.form.get('clearance_price', 0))
        
        # Validate numeric inputs
        if any(cost < 0 for cost in [price_per_kg, packaging_price, kuwait_transport_price, sudan_transport_price, clearance_price]):
            return jsonify({'success': False, 'message': 'جميع الأسعار يجب أن تكون أكبر من أو تساوي صفر'})
        
        # Create or update air shipping costs
        from models import AirShippingCosts
        AirShippingCosts.create_or_update_costs(
            price_per_kg=price_per_kg,
            packaging_price=packaging_price,
            kuwait_transport_price=kuwait_transport_price,
            sudan_transport_price=sudan_transport_price,
            clearance_price=clearance_price,
            admin_id=current_user.id
        )
        
        return jsonify({
            'success': True, 
            'message': 'تم حفظ تكاليف الشحن الجوي بنجاح'
        })
        
    except ValueError:
        return jsonify({'success': False, 'message': 'يرجى إدخال قيم رقمية صحيحة'})
    except Exception as e:
        logging.error(f'Error updating air shipping costs: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء حفظ التكاليف'})


@app.route('/api/price_per_kg')
@login_required
def get_price_per_kg():
    """Get current price per kg setting"""
    try:
        # Get price per kg from session or GlobalSettings
        price_per_kg = session.get('price_per_kg', 0.000)
        if price_per_kg == 0.000:
            price_per_kg = GlobalSettings.get_setting('price_per_kg', 0.000)
        
        return jsonify({
            'success': True,
            'price_per_kg': float(price_per_kg)
        })
    except Exception as e:
        logging.error(f'Error getting price per kg: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ في تحميل سعر الكيلو'})


@app.route('/api/air_shipping_costs')
@login_required
@permission_required('expenses')
def get_air_shipping_costs():
    """Get current air shipping costs configuration"""
    try:
        from models import AirShippingCosts
        costs = AirShippingCosts.get_current_costs()
        
        if costs:
            return jsonify({
                'success': True,
                'costs': {
                    'price_per_kg': costs.price_per_kg,
                    'packaging_price': costs.packaging_price,
                    'kuwait_transport_price': costs.kuwait_transport_price,
                    'sudan_transport_price': costs.sudan_transport_price,
                    'clearance_price': costs.clearance_price
                }
            })
        else:
            return jsonify({
                'success': True,
                'costs': {
                    'price_per_kg': 0.0,
                    'packaging_price': 0.0,
                    'kuwait_transport_price': 0.0,
                    'sudan_transport_price': 0.0,
                    'clearance_price': 0.0
                }
            })
    except Exception as e:
        logging.error(f'Error getting air shipping costs: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ في تحميل التكاليف'})


@app.route('/update_document_costs', methods=['POST'])
@login_required
@permission_required('expenses')
def update_document_costs():
    """Update document costs configuration"""
    try:
        from models import DocumentCosts
        
        # Get form data with safe float conversion
        def safe_float_conversion(value):
            try:
                return float(value) if value else 0.0
            except (ValueError, TypeError):
                return 0.0
        
        doc_authentication_foreign = safe_float_conversion(request.form.get('doc_authentication_foreign'))
        doc_authentication_education = safe_float_conversion(request.form.get('doc_authentication_education'))
        doc_criminal_record = safe_float_conversion(request.form.get('doc_criminal_record'))
        doc_secondary_certificate = safe_float_conversion(request.form.get('doc_secondary_certificate'))
        doc_university_certificate = safe_float_conversion(request.form.get('doc_university_certificate'))
        doc_marriage_registered = safe_float_conversion(request.form.get('doc_marriage_registered'))
        doc_marriage_unregistered = safe_float_conversion(request.form.get('doc_marriage_unregistered'))
        doc_university_details = safe_float_conversion(request.form.get('doc_university_details'))
        
        # Create new document costs configuration
        DocumentCosts.create_or_update_costs(
            doc_authentication_foreign=doc_authentication_foreign,
            doc_authentication_education=doc_authentication_education,
            doc_criminal_record=doc_criminal_record,
            doc_secondary_certificate=doc_secondary_certificate,
            doc_university_certificate=doc_university_certificate,
            doc_marriage_registered=doc_marriage_registered,
            doc_marriage_unregistered=doc_marriage_unregistered,
            doc_university_details=doc_university_details,
            admin_id=current_user.id
        )
        
        return jsonify({
            'success': True,
            'message': 'تم حفظ إعدادات تكاليف المستندات بنجاح'
        })
        
    except Exception as e:
        logging.error(f'Error updating document costs: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء حفظ إعدادات التكاليف'
        })


@app.route('/api/document_costs')
@login_required
@permission_required('expenses')
def get_document_costs():
    """Get current document costs configuration"""
    try:
        from models import DocumentCosts
        costs = DocumentCosts.get_current_costs()
        
        if costs:
            return jsonify({
                'success': True,
                'costs': {
                    'doc_authentication_foreign': costs.doc_authentication_foreign,
                    'doc_authentication_education': costs.doc_authentication_education,
                    'doc_criminal_record': costs.doc_criminal_record,
                    'doc_secondary_certificate': costs.doc_secondary_certificate,
                    'doc_university_certificate': costs.doc_university_certificate,
                    'doc_marriage_registered': costs.doc_marriage_registered,
                    'doc_marriage_unregistered': costs.doc_marriage_unregistered,
                    'doc_university_details': costs.doc_university_details
                }
            })
        else:
            return jsonify({
                'success': True,
                'costs': {
                    'doc_authentication_foreign': 0.0,
                    'doc_authentication_education': 0.0,
                    'doc_criminal_record': 0.0,
                    'doc_secondary_certificate': 0.0,
                    'doc_university_certificate': 0.0,
                    'doc_marriage_registered': 0.0,
                    'doc_marriage_unregistered': 0.0,
                    'doc_university_details': 0.0
                }
            })
    except Exception as e:
        logging.error(f'Error getting document costs: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ في تحميل التكاليف'})





@app.route('/api/automatic_revenues')
@login_required
@permission_required('expenses')
def get_automatic_revenues():
    """Get automatic revenues calculated from shipments database"""
    try:
        from datetime import datetime
        
        # Get date filters from request
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        
        # Parse dates
        start_date = None
        end_date = None
        
        try:
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            start_date = end_date = None
        
        # Get all shipments in the date range
        if start_date and end_date:
            shipments_query = Shipment.query.filter(
                Shipment.created_at >= start_date,
                Shipment.created_at <= end_date
            )
        else:
            shipments_query = Shipment.query
        
        all_shipments = shipments_query.all()
        
        # Categorize shipments
        general_shipments = [s for s in all_shipments if s.package_type != 'document']
        document_shipments = [s for s in all_shipments if s.package_type == 'document']
        
        # Further categorize by shipping method
        air_shipments = [s for s in general_shipments if s.shipping_method == 'جوي']
        land_shipments = [s for s in general_shipments if s.shipping_method == 'بري']
        
        # Calculate revenues from paid amounts
        air_shipping_revenue = sum([float(s.paid_amount or 0) for s in air_shipments])
        land_shipping_revenue = sum([float(s.paid_amount or 0) for s in land_shipments])
        documents_revenue = sum([float(s.paid_amount or 0) for s in document_shipments])
        
        general_shipments_revenue = air_shipping_revenue + land_shipping_revenue
        total_revenue = general_shipments_revenue + documents_revenue
        
        return jsonify({
            'success': True,
            'air_shipping_revenue': round(air_shipping_revenue, 3),
            'land_shipping_revenue': round(land_shipping_revenue, 3),
            'general_shipments_revenue': round(general_shipments_revenue, 3),
            'documents_revenue': round(documents_revenue, 3),
            'total_revenue': round(total_revenue, 3),
            'air_shipments_count': len(air_shipments),
            'land_shipments_count': len(land_shipments),
            'document_shipments_count': len(document_shipments),
            'general_shipments_count': len(general_shipments)
        })
        
    except Exception as e:
        logging.error(f'Error calculating automatic revenues: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'خطأ في حساب الإيرادات التلقائية'
        })








@app.route('/api/air_shipping_revenue')
@login_required
@permission_required('expenses')
def api_air_shipping_revenue():
    """API endpoint for air shipping revenue data from all shipments"""
    try:
        # Query air shipping revenue from all general shipments with shipping_method = 'جوي'
        air_shipments = Shipment.query.filter(
            Shipment.package_type != 'document',
            Shipment.shipping_method == 'جوي'
        ).all()
        
        # Calculate total using paid_amount field (actual revenue received)
        total_air_revenue = sum(float(shipment.paid_amount or 0) for shipment in air_shipments)
        
        return jsonify({
            'success': True,
            'total': total_air_revenue,
            'count': len(air_shipments)
        })
    
    except Exception as e:
        app.logger.error(f'Error getting air shipping revenue: {str(e)}')
        return jsonify({'success': False, 'total': 0, 'count': 0})


@app.route('/api/land_shipping_revenue')
@login_required
@permission_required('expenses')
def api_land_shipping_revenue():
    """API endpoint for land shipping revenue data from all shipments"""
    try:
        # Query land shipping revenue from all general shipments with shipping_method = 'بري'
        land_shipments = Shipment.query.filter(
            Shipment.package_type != 'document',
            Shipment.shipping_method == 'بري'
        ).all()
        
        # Calculate total using paid_amount field (actual revenue received)
        total_land_revenue = sum(float(shipment.paid_amount or 0) for shipment in land_shipments)
        
        return jsonify({
            'success': True,
            'total': total_land_revenue,
            'count': len(land_shipments)
        })
    
    except Exception as e:
        app.logger.error(f'Error getting land shipping revenue: {str(e)}')
        return jsonify({'success': False, 'total': 0, 'count': 0})


@app.route('/api/document_shipping_revenue')
@login_required
@permission_required('expenses')
def api_document_shipping_revenue():
    """API endpoint for document shipping revenue data from all shipments"""
    try:
        # Query document shipping revenue from all document shipments
        document_shipments = Shipment.query.filter(
            Shipment.package_type == 'document'
        ).all()
        
        # Calculate total using paid_amount field (actual revenue received)
        total_document_revenue = sum(float(shipment.paid_amount or 0) for shipment in document_shipments)
        
        return jsonify({
            'success': True,
            'total': total_document_revenue,
            'count': len(document_shipments)
        })
    
    except Exception as e:
        app.logger.error(f'Error getting document shipping revenue: {str(e)}')
        return jsonify({'success': False, 'total': 0, 'count': 0})


@app.route('/api/recent_expenses')
@login_required
@permission_required('expenses')
def get_recent_expenses():
    """Get recent expenses for display"""
    try:
        # Get last 5 expenses
        recent_expenses = FinancialTransaction.query.filter_by(
            transaction_type='expense'
        ).order_by(FinancialTransaction.created_at.desc()).limit(5).all()
        
        expenses_data = []
        total_amount = 0
        
        for expense in recent_expenses:
            amount = float(expense.amount or 0)
            expenses_data.append({
                'id': expense.id,
                'name': expense.name,
                'amount': amount,
                'category': expense.category or '',
                'created_at': expense.created_at.strftime('%Y-%m-%d') if expense.created_at else ''
            })
            total_amount += amount
        
        return jsonify({
            'success': True,
            'expenses': expenses_data,
            'total': total_amount
        })
        
    except Exception as e:
        logging.error(f'Error getting recent expenses: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/get_all_revenues')
@login_required
def get_all_revenues():
    """Get all revenue data in one call"""
    try:
        # Calculate air shipping revenue
        air_shipments = Shipment.query.filter(
            Shipment.shipping_method == 'جوي',
            Shipment.package_type != 'document'
        ).all()
        air_revenue = sum(float(s.paid_amount or 0) for s in air_shipments)
        
        # Calculate land shipping revenue  
        land_shipments = Shipment.query.filter(
            Shipment.shipping_method == 'بري',
            Shipment.package_type != 'document'
        ).all()
        land_revenue = sum(float(s.paid_amount or 0) for s in land_shipments)
        
        # Calculate document shipping revenue
        document_shipments = Shipment.query.filter(
            Shipment.package_type == 'document'
        ).all()
        document_revenue = sum(float(s.paid_amount or 0) for s in document_shipments)
        
        total_revenue = air_revenue + land_revenue + document_revenue
        
        return jsonify({
            'success': True,
            'air_revenue': air_revenue,
            'land_revenue': land_revenue,
            'document_revenue': document_revenue,
            'total_revenue': total_revenue
        })
        
    except Exception as e:
        logging.error(f'Error getting all revenues: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/delete_shipment_type/<int:type_id>', methods=['POST'])
@login_required
def delete_shipment_type(type_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لحذف أنواع الشحنات', 'error')
        return redirect(url_for('index'))
    
    try:
        shipment_type = ShipmentType.query.get_or_404(type_id)
        
        # Soft delete by setting is_active to False
        shipment_type.is_active = False
        db.session.commit()
        
        flash(f'تم حذف نوع الشحنة "{shipment_type.name_ar}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء حذف نوع الشحنة', 'error')
    
    return redirect(url_for('settings') + '#types')


@app.route('/delete_document_type/<int:type_id>', methods=['POST'])
@login_required
def delete_document_type(type_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لحذف أنواع الوثائق', 'error')
        return redirect(url_for('index'))
    
    try:
        document_type = DocumentType.query.get_or_404(type_id)
        
        # Soft delete by setting is_active to False
        document_type.is_active = False
        db.session.commit()
        
        flash(f'تم حذف نوع الوثيقة "{document_type.name_ar}" بنجاح', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء حذف نوع الوثيقة', 'error')
    
    return redirect(url_for('settings') + '#pricing')


# Pricing Management Routes
@app.route('/pricing_management')
@login_required
def pricing_management():
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('index'))
    
    shipment_types = ShipmentType.query.filter_by(is_active=True).order_by(ShipmentType.name_ar).all()
    document_types = DocumentType.query.filter_by(is_active=True).order_by(DocumentType.name_ar).all()
    
    # Calculate average prices
    avg_shipment_price = db.session.query(db.func.avg(ShipmentType.price)).filter_by(is_active=True).scalar() or 0
    avg_document_price = db.session.query(db.func.avg(DocumentType.price)).filter_by(is_active=True).scalar() or 0
    
    return render_template('pricing_management.html',
                         shipment_types=shipment_types,
                         document_types=document_types,
                         avg_shipment_price=avg_shipment_price,
                         avg_document_price=avg_document_price)


@app.route('/update_shipment_price/<int:type_id>', methods=['POST'])
@login_required
def update_shipment_price(type_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لتحديث الأسعار', 'error')
        return redirect(url_for('index'))
    
    try:
        shipment_type = ShipmentType.query.get_or_404(type_id)
        
        price = request.form.get('price', '').strip()
        if not price:
            flash('يرجى إدخال السعر', 'error')
            return redirect(url_for('settings') + '#pricing')
        
        try:
            price_value = float(price)
            if price_value < 0:
                flash('السعر يجب أن يكون أكبر من أو يساوي صفر', 'error')
                return redirect(url_for('settings') + '#pricing')
        except ValueError:
            flash('يرجى إدخال سعر صحيح', 'error')
            return redirect(url_for('settings') + '#pricing')
        
        old_price = shipment_type.price
        shipment_type.price = price_value
        db.session.commit()
        
        flash(f'تم تحديث سعر "{shipment_type.name_ar}" من {old_price:.2f} د.ك إلى {price_value:.2f} د.ك', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء تحديث السعر', 'error')
    
    return redirect(url_for('settings') + '#pricing')


@app.route('/update_document_price/<int:type_id>', methods=['POST'])
@login_required
def update_document_price(type_id):
    if not current_user.is_super_admin:
        flash('ليس لديك صلاحية لتحديث الأسعار', 'error')
        return redirect(url_for('index'))
    
    try:
        document_type = DocumentType.query.get_or_404(type_id)
        
        price = request.form.get('price', '').strip()
        if not price:
            flash('يرجى إدخال السعر', 'error')
            return redirect(url_for('settings') + '#pricing')
        
        try:
            price_value = float(price)
            if price_value < 0:
                flash('السعر يجب أن يكون أكبر من أو يساوي صفر', 'error')
                return redirect(url_for('settings') + '#pricing')
        except ValueError:
            flash('يرجى إدخال سعر صحيح', 'error')
            return redirect(url_for('settings') + '#pricing')
        
        old_price = document_type.price
        document_type.price = price_value
        db.session.commit()
        
        flash(f'تم تحديث سعر "{document_type.name_ar}" من {old_price:.2f} د.ك إلى {price_value:.2f} د.ك', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء تحديث السعر', 'error')
    
    return redirect(url_for('settings') + '#pricing')

# Price per KG Route
@app.route('/update_price_per_kg', methods=['POST'])
@login_required
@permission_required('Home')
def update_price_per_kg():
    """Update global price per kg setting"""
    try:
        price_per_kg = float(request.form.get('price_per_kg', 0))
        
        # Store in session or database - for now using session
        session['price_per_kg'] = price_per_kg
        
        flash(f'تم تحديث سعر الكيلو إلى {price_per_kg:.3f} د.ك', 'success')
    except ValueError:
        flash('يرجى إدخال قيمة صحيحة للسعر', 'error')
    except Exception as e:
        flash('حدث خطأ أثناء تحديث السعر', 'error')
    
    return redirect(url_for('settings') + '#pricing')


# Additional Pricing Routes
@app.route('/update_packaging_price', methods=['POST'])
@login_required
@permission_required('Home')
def update_packaging_price():
    """Update global packaging price setting"""
    try:
        packaging_price = float(request.form.get('packaging_price', 0))
        
        # Save to GlobalSettings table
        GlobalSettings.set_setting('packaging_price', packaging_price)
        
        flash(f'تم تحديث سعر التغليف إلى {packaging_price:.3f} د.ك', 'success')
    except ValueError:
        flash('يرجى إدخال قيمة صحيحة للسعر', 'error')
    except Exception as e:
        flash('حدث خطأ أثناء تحديث السعر', 'error')
    
    return redirect(url_for('settings') + '#pricing')


@app.route('/update_waybill_price', methods=['POST'])
@login_required
@permission_required('Home')
def update_waybill_price():
    """Update global waybill price setting"""
    try:
        waybill_price = float(request.form.get('waybill_price', 0))
        
        # Save to GlobalSettings table
        GlobalSettings.set_setting('waybill_price', waybill_price)
        
        flash(f'تم تحديث سعر البوليصة إلى {waybill_price:.3f} د.ك', 'success')
    except ValueError:
        flash('يرجى إدخال قيمة صحيحة للسعر', 'error')
    except Exception as e:
        flash('حدث خطأ أثناء تحديث السعر', 'error')
    
    return redirect(url_for('settings') + '#pricing')


# Edit Shipment Routes
@app.route("/edit_shipment/<int:shipment_id>", methods=['GET'])
@login_required
@permission_required("Home")
def edit_shipment(shipment_id):
    """Edit shipment form"""
    shipment = Shipment.query.get_or_404(shipment_id)
    
    # GET request - show edit form
    shipment_types = ShipmentType.query.filter_by(is_active=True).order_by(ShipmentType.name_ar).all()
    document_types = DocumentType.query.filter_by(is_active=True).order_by(DocumentType.name_ar).all()
    zone_pricings = ZonePricing.query.filter_by(is_active=True).order_by(ZonePricing.zone_name_ar).all()
    packaging_types = PackagingType.query.filter_by(is_active=True).order_by(PackagingType.name_ar).all()
    
    # Convert zone_pricings to dict for JSON serialization
    zone_pricings_dict = [
        {
            'id': zp.id,
            'zone_name_ar': zp.zone_name_ar,
            'zone_name_en': zp.zone_name_en,
            'price_per_kg': float(zp.price_per_kg),
            'direction': zp.direction
        } for zp in zone_pricings
    ]
    
    return render_template("edit_shipment.html", 
                         shipment=shipment,
                         shipment_types=shipment_types,
                         document_types=document_types,
                         zone_pricings=zone_pricings_dict,
                         packaging_types=packaging_types)

@app.route("/update_shipment/<int:shipment_id>", methods=["POST"])
@login_required
@permission_required("Home")
def update_shipment(shipment_id):
    """Update shipment"""
    shipment = Shipment.query.get_or_404(shipment_id)
    
    try:
        # Get form data with defaults
        sender_name = request.form.get('sender_name', '').strip() or 'غير محدد'
        sender_phone = request.form.get('sender_phone', '').strip() or 'غير محدد'
        sender_address = request.form.get('sender_address', '').strip()
        sender_email = request.form.get('sender_email', '').strip()
        
        receiver_name = request.form.get('receiver_name', '').strip() or 'غير محدد'
        receiver_phone = request.form.get('receiver_phone', '').strip() or 'غير محدد'
        receiver_address = request.form.get('receiver_address', '').strip()
        receiver_email = request.form.get('receiver_email', '').strip()
        
        direction = request.form.get('direction', '').strip() or 'kuwait_to_sudan'
        package_type = request.form.get('package_type', '').strip() or 'general'
        package_contents = request.form.get('package_contents', '').strip()
        action_required = request.form.get('action_required', '').strip()
        document_type = request.form.get('document_type', '').strip()
        zone = request.form.get('zone', '').strip()
        shipping_method = request.form.get('shipping_method', '').strip()
        weight_str = request.form.get('weight', '').strip()
        price_str = request.form.get('total_price', '').strip()
        discount_str = request.form.get('discount', '0').strip()
        paid_amount_str = request.form.get('amount_paid', '0').strip()
        notes = request.form.get('notes', '').strip()
        
        # Get checkbox values
        has_packaging = bool(request.form.get('has_packaging'))
        has_policy = bool(request.form.get('has_policy'))
        has_comment = bool(request.form.get('has_comment'))
        waybill_price_str = request.form.get('waybill_price', '0').strip()
        cost_str = request.form.get('cost', '0').strip()
        profit_str = request.form.get('profit', '0').strip()
        
        # Process numeric fields
        weight = 0.0
        price = 0.0
        discount = 0.0
        paid_amount = 0.0
        waybill_price = 0.0
        cost = 0.0
        profit = 0.0
        
        try:
            weight = float(weight_str) if weight_str else 0.0
        except ValueError:
            weight = 0.0
            
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            price = 0.0
            
        try:
            discount = float(discount_str) if discount_str else 0.0
        except ValueError:
            discount = 0.0
            
        try:
            paid_amount = float(paid_amount_str) if paid_amount_str else 0.0
        except ValueError:
            paid_amount = 0.0
            
        try:
            waybill_price = float(waybill_price_str) if waybill_price_str else 0.0
        except ValueError:
            waybill_price = 0.0
            
        try:
            cost = float(cost_str) if cost_str else 0.0
        except ValueError:
            cost = 0.0
            
        try:
            profit = float(profit_str) if profit_str else 0.0
        except ValueError:
            profit = 0.0
        
        # For documents, store action_required in package_contents
        if package_type == 'document' and action_required:
            package_contents = action_required
        
        # Calculate remaining amount
        remaining_amount = price - paid_amount
        
        # Update shipment fields (preserve tracking number)
        shipment.sender_name = sender_name
        shipment.sender_phone = sender_phone
        shipment.sender_address = sender_address
        shipment.sender_email = sender_email
        
        shipment.receiver_name = receiver_name
        shipment.receiver_phone = receiver_phone
        shipment.receiver_address = receiver_address
        shipment.receiver_email = receiver_email
        
        shipment.direction = direction
        shipment.package_type = package_type
        shipment.package_contents = package_contents
        shipment.document_type = document_type if package_type == 'document' else None
        shipment.zone = zone
        shipment.shipping_method = shipping_method
        shipment.weight = weight
        shipment.price = price
        shipment.discount = discount
        shipment.cost = cost
        shipment.profit = profit
        shipment.paid_amount = paid_amount
        shipment.remaining_amount = remaining_amount
        shipment.has_packaging = has_packaging
        shipment.has_policy = has_policy
        shipment.has_comment = has_comment
        shipment.waybill_price = waybill_price
        shipment.notes = notes
        
        db.session.commit()
        flash("تم تحديث الشحنة بنجاح", "success")
        logging.info(f'Shipment updated: {shipment.tracking_number}')
        return redirect(url_for("index"))
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error updating shipment: {str(e)}')
        flash("حدث خطأ أثناء تحديث الشحنة", "error")
        return redirect(url_for("edit_shipment", shipment_id=shipment_id))

# API Endpoints for dynamic pricing
@app.route("/api/get_shipment_price")
@login_required
def get_shipment_price():
    """Get price for a shipment type"""
    shipment_type_name = request.args.get("type")
    direction = request.args.get("direction")
    
    if not shipment_type_name:
        return jsonify({"error": "Missing shipment type"}), 400
    
    # Find shipment type by name_en
    shipment_type = ShipmentType.query.filter_by(name_en=shipment_type_name).first()
    
    if not shipment_type:
        return jsonify({"error": "Shipment type not found"}), 404
    
    return jsonify({
        "price": shipment_type.price,
        "type_name": shipment_type.name_ar
    })

@app.route("/api/get_document_price")
@login_required
def get_document_price():
    """Get price for a document type"""
    document_type_name = request.args.get("type")
    
    if not document_type_name:
        return jsonify({"error": "Missing document type"}), 400
    
    # Find document type by name_en
    document_type = DocumentType.query.filter_by(name_en=document_type_name).first()
    
    if not document_type:
        return jsonify({"error": "Document type not found"}), 404
    
    return jsonify({
        "price": document_type.price,
        "type_name": document_type.name_ar
    })


@app.route('/api/get_zone_pricing')
@login_required
def get_zone_pricing():
    """Get pricing for a specific zone and direction"""
    zone_name = request.args.get('zone', '').strip()
    direction = request.args.get('direction', '').strip()
    
    if not zone_name or not direction:
        return jsonify({'error': 'Zone and direction are required'}), 400
    
    try:
        # Get zone pricing from database
        zone_pricing = ZonePricing.query.filter_by(
            zone_name_en=zone_name, 
            direction=direction, 
            is_active=True
        ).first()
        
        if not zone_pricing:
            return jsonify({'error': 'Zone pricing not found'}), 404
        
        return jsonify({
            'price_per_kg': float(zone_pricing.price_per_kg),
            'zone_name': zone_pricing.zone_name_ar,
            'direction': zone_pricing.direction,
            'success': True
        })
        
    except Exception as e:
        logging.error(f'Error getting zone pricing: {str(e)}')
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/get_packaging_cost')
@login_required
def get_packaging_cost():
    """Get cost for a specific packaging type"""
    packaging_type = request.args.get('type', '').strip()
    
    if not packaging_type:
        return jsonify({'error': 'Packaging type is required'}), 400
    
    try:
        # Get packaging type from database
        packaging = PackagingType.query.filter_by(name_en=packaging_type, is_active=True).first()
        
        if not packaging:
            return jsonify({'error': 'Packaging type not found'}), 404
        
        return jsonify({
            'cost': float(packaging.cost),
            'type_name': packaging.name_ar,
            'success': True
        })
        
    except Exception as e:
        logging.error(f'Error getting packaging cost: {str(e)}')
        return jsonify({'error': 'Server error'}), 500


@app.route('/delete_shipment/<int:shipment_id>', methods=['POST'])
@login_required
@permission_required('Home')
def delete_shipment(shipment_id):
    """Delete a shipment"""
    try:
        shipment = Shipment.query.get(shipment_id)
        
        if not shipment:
            logging.warning(f'Attempted to delete non-existent shipment: {shipment_id}')
            return jsonify({
                'success': False, 
                'error': 'الشحنة غير موجودة أو تم حذفها مسبقاً',
                'error_type': 'not_found'
            }), 404
        
        tracking_number = shipment.tracking_number
        
        # Delete the shipment
        db.session.delete(shipment)
        db.session.commit()
        
        logging.info(f'Shipment deleted: {tracking_number} by user {current_user.username}')
        return jsonify({
            'success': True, 
            'message': f'تم حذف الشحنة {tracking_number} بنجاح',
            'tracking_number': tracking_number
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting shipment {shipment_id}: {str(e)}')
        return jsonify({
            'success': False, 
            'error': f'حدث خطأ أثناء حذف الشحنة: {str(e)}',
            'error_type': 'server_error'
        }), 500


@app.route('/api/process_payment', methods=['POST'])
@login_required
@permission_required('Home')
def process_payment():
    """Process payment for a shipment"""
    try:
        data = request.get_json()
        shipment_id = data.get('shipment_id')
        payment_amount = float(data.get('payment_amount', 0))
        
        if not shipment_id:
            return jsonify({'success': False, 'message': 'معرف الشحنة مطلوب'})
        
        if payment_amount <= 0:
            return jsonify({'success': False, 'message': 'مبلغ الدفع يجب أن يكون أكبر من صفر'})
        
        # Get shipment
        shipment = Shipment.query.get(shipment_id)
        if not shipment:
            return jsonify({'success': False, 'message': 'الشحنة غير موجودة'})
        
        # Calculate new amounts
        current_paid = shipment.paid_amount if shipment.paid_amount else 0.0
        current_remaining = shipment.remaining_amount if shipment.remaining_amount is not None else 0.0
        
        # Validate payment amount doesn't exceed remaining
        if payment_amount > current_remaining:
            return jsonify({'success': False, 'message': 'مبلغ الدفع أكبر من المبلغ المتبقي'})
        
        # Update amounts
        new_paid_amount = current_paid + payment_amount
        new_remaining_amount = current_remaining - payment_amount
        
        shipment.paid_amount = new_paid_amount
        shipment.remaining_amount = new_remaining_amount
        
        # Commit changes
        db.session.commit()
        
        # Check if fully paid
        fully_paid = new_remaining_amount <= 0.001  # Use small epsilon for float comparison
        
        if fully_paid:
            message = f'تم إكمال دفع الشحنة {shipment.tracking_number} بنجاح'
        else:
            message = f'تم دفع {payment_amount:.3f} د.ك للشحنة {shipment.tracking_number}'
        
        return jsonify({
            'success': True,
            'message': message,
            'fully_paid': fully_paid,
            'new_paid_amount': new_paid_amount,
            'new_remaining_amount': new_remaining_amount,
            'tracking_number': shipment.tracking_number
        })
        
    except ValueError:
        return jsonify({'success': False, 'message': 'مبلغ الدفع يجب أن يكون رقماً صحيحاً'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error processing payment: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء معالجة الدفع'})





@app.route('/print_invoice/<int:shipment_id>')
@login_required
def print_invoice(shipment_id):
    """Print invoice for a specific shipment"""
    shipment = Shipment.query.get_or_404(shipment_id)
    
    return render_template('professional_invoice.html', shipment=shipment)



@app.route('/print_sticker/<int:shipment_id>')
@login_required
def print_sticker(shipment_id):
    """Print sticker for a specific shipment"""
    shipment = Shipment.query.get_or_404(shipment_id)
    
    return render_template('print_sticker.html', shipment=shipment)

@app.route('/api/clear_all_expenses', methods=['POST'])
@login_required
@permission_required('expenses')
def clear_all_expenses():
    """Clear all expense data from the Financial Center"""
    try:
        # Delete all financial transactions of type 'expense'
        deleted_count = FinancialTransaction.query.filter_by(transaction_type='expense').count()
        FinancialTransaction.query.filter_by(transaction_type='expense').delete()
        db.session.commit()
        
        logging.info(f"Admin {current_user.username} cleared all expenses ({deleted_count} records)")
        
        return jsonify({
            'success': True,
            'message': f'تم مسح {deleted_count} مصروف بنجاح',
            'deleted_count': deleted_count
        })
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error clearing all expenses: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء مسح المصروفات'
        }), 500


# Expense Management Routes
@app.route('/add_expense_general', methods=['POST'])
@login_required
@permission_required('expenses')
def add_expense_general():
    """Add a new general expense"""
    try:
        name = request.form.get('name', '').strip()
        amount_str = request.form.get('amount', '').strip()
        notes = request.form.get('notes', '').strip()
        expense_date_str = request.form.get('expense_date', '').strip()
        shipment_id = request.form.get('shipment_id') or None
        
        # Validate inputs
        if not name:
            return jsonify({'success': False, 'message': 'يرجى إدخال اسم المصروف'})
        
        if not amount_str:
            return jsonify({'success': False, 'message': 'يرجى إدخال المبلغ'})
        
        if not expense_date_str:
            return jsonify({'success': False, 'message': 'يرجى تحديد تاريخ المصروف'})
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون أكبر من صفر'})
        except ValueError:
            return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون رقماً صحيحاً'})
        
        try:
            expense_date = datetime.strptime(expense_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'تنسيق التاريخ غير صحيح'})
        
        # Create new expense  
        expense = ExpenseGeneral(
            name=name,
            amount=amount,
            notes=notes if notes else None,
            expense_date=expense_date,
            shipment_id=int(shipment_id) if shipment_id else None
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حفظ المصروف بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error adding general expense: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في حفظ المصروف: {str(e)}'})


@app.route('/add_expense_documents', methods=['POST'])
@login_required
@permission_required('expenses')
def add_expense_documents():
    """Add a new document expense"""
    try:
        name = request.form.get('name', '').strip()
        amount_str = request.form.get('amount', '').strip()
        notes = request.form.get('notes', '').strip()
        expense_date_str = request.form.get('expense_date', '').strip()
        shipment_id = request.form.get('shipment_id') or None
        
        # Validate inputs
        if not name:
            return jsonify({'success': False, 'message': 'يرجى إدخال اسم المصروف'})
        
        if not amount_str:
            return jsonify({'success': False, 'message': 'يرجى إدخال المبلغ'})
        
        if not expense_date_str:
            return jsonify({'success': False, 'message': 'يرجى تحديد تاريخ المصروف'})
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون أكبر من صفر'})
        except ValueError:
            return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون رقماً صحيحاً'})
        
        try:
            expense_date = datetime.strptime(expense_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'تنسيق التاريخ غير صحيح'})
        
        # Create new expense
        expense = ExpenseDocuments(
            name=name,
            amount=amount,
            notes=notes if notes else None,
            expense_date=expense_date,
            shipment_id=int(shipment_id) if shipment_id else None
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حفظ المصروف بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error adding document expense: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في حفظ المصروف: {str(e)}'})


# General Shipments Expenses Routes
@app.route('/add_expense_general_shipments', methods=['POST'])
@login_required
@permission_required('expenses')
def add_expense_general_shipments():
    """Add a new general shipments expense"""
    try:
        name = request.form.get('name', '').strip()
        amount_str = request.form.get('amount', '').strip()
        notes = request.form.get('notes', '').strip()
        expense_date_str = request.form.get('expense_date', '').strip()
        
        if not name or not amount_str or not expense_date_str:
            return jsonify({'success': False, 'message': 'جميع الحقول مطلوبة'})
        
        # Convert amount to float
        try:
            amount = float(amount_str)
            if amount <= 0:
                return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون أكبر من صفر'})
        except ValueError:
            return jsonify({'success': False, 'message': 'المبلغ غير صحيح'})
        
        # Parse date
        try:
            expense_date = datetime.strptime(expense_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'تاريخ غير صحيح'})
        
        # Create new expense with shipping_type for general shipments
        expense = FinancialTransaction(
            name=name,
            amount=amount,
            transaction_type='expense',
            shipping_type='شحنات عامة',
            category='شحنات عامة',
            description=notes if notes else None,
            transaction_date=datetime.combine(expense_date, datetime.min.time()),
            admin_id=current_user.id
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حفظ مصروف الشحنات العامة بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error adding general shipments expense: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في حفظ المصروف: {str(e)}'})


@app.route('/api/expenses_general_shipments')
@login_required
@permission_required('expenses')
def get_expenses_general_shipments():
    """Get all general shipments expenses"""
    try:
        expenses = FinancialTransaction.query.filter_by(
            transaction_type='expense',
            shipping_type='شحنات عامة'
        ).order_by(FinancialTransaction.transaction_date.desc()).all()
        
        expenses_data = []
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'name': expense.name,
                'amount': float(expense.amount),
                'notes': expense.description,
                'date': expense.transaction_date.strftime('%Y-%m-%d')
            })
        
        return jsonify({'success': True, 'expenses': expenses_data})
        
    except Exception as e:
        logging.error(f'Error fetching general shipments expenses: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في جلب المصروفات: {str(e)}'})


@app.route('/delete_expense_general_shipments/<int:expense_id>', methods=['DELETE'])
@login_required
@permission_required('expenses')
def delete_expense_general_shipments(expense_id):
    """Delete a general shipments expense"""
    try:
        expense = FinancialTransaction.query.filter_by(
            id=expense_id,
            transaction_type='expense',
            shipping_type='شحنات عامة'
        ).first()
        
        if not expense:
            return jsonify({'success': False, 'message': 'المصروف غير موجود'})
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف مصروف الشحنات العامة بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting general shipments expense: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في حذف المصروف: {str(e)}'})


@app.route('/api/expenses_general')
@login_required
@permission_required('expenses')
def get_expenses_general():
    """Get all general expenses"""
    try:
        expenses = ExpenseGeneral.query.order_by(ExpenseGeneral.expense_date.desc()).all()
        expenses_data = []
        
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'name': expense.name,
                'amount': float(expense.amount),
                'notes': expense.notes,
                'expense_date': expense.expense_date.strftime('%Y-%m-%d'),
                'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return jsonify({'success': True, 'expenses': expenses_data})
        
    except Exception as e:
        logging.error(f'Error fetching general expenses: {str(e)}')
        return jsonify({'success': False, 'message': 'خطأ في تحميل المصروفات'})


@app.route('/api/expenses_documents')
@login_required
@permission_required('expenses')
def get_expenses_documents():
    """Get all document expenses"""
    try:
        expenses = ExpenseDocuments.query.order_by(ExpenseDocuments.expense_date.desc()).all()
        expenses_data = []
        
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'name': expense.name,
                'amount': float(expense.amount),
                'notes': expense.notes,
                'expense_date': expense.expense_date.strftime('%Y-%m-%d'),
                'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return jsonify({'success': True, 'expenses': expenses_data})
        
    except Exception as e:
        logging.error(f'Error fetching document expenses: {str(e)}')
        return jsonify({'success': False, 'message': 'خطأ في تحميل المصروفات'})


@app.route('/delete_expense_general/<int:expense_id>', methods=['POST'])
@login_required
@permission_required('expenses')
def delete_expense_general(expense_id):
    """Delete a general expense"""
    try:
        expense = ExpenseGeneral.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف المصروف بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting general expense: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ في حذف المصروف'})


@app.route('/delete_expense_documents/<int:expense_id>', methods=['POST'])
@login_required
@permission_required('expenses')
def delete_expense_documents(expense_id):
    """Delete a document expense"""
    try:
        expense = ExpenseDocuments.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف المصروف بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting document expense: {str(e)}')
        return jsonify({'success': False, 'message': 'حدث خطأ في حذف المصروف'})


@app.route('/api/total_expenses')
@login_required
@permission_required('expenses')
def api_total_expenses():
    """Calculate total expenses from office, general shipments, and document expenses"""
    try:
        from sqlalchemy import func
        
        # Calculate total office expenses (ExpenseGeneral)
        office_total = db.session.query(func.sum(ExpenseGeneral.amount)).scalar() or 0
        
        # Calculate total general shipments expenses (FinancialTransaction with shipping_type = 'شحنات عامة')
        general_shipments_total = db.session.query(func.sum(FinancialTransaction.amount)).filter_by(
            transaction_type='expense',
            shipping_type='شحنات عامة'
        ).scalar() or 0
        
        # Calculate total document expenses
        document_total = db.session.query(func.sum(ExpenseDocuments.amount)).scalar() or 0
        
        # Calculate grand total
        grand_total = float(office_total) + float(general_shipments_total) + float(document_total)
        
        return jsonify({
            'success': True,
            'office_total': float(office_total),
            'general_shipments_total': float(general_shipments_total),
            'document_total': float(document_total),
            'grand_total': grand_total
        })
    except Exception as e:
        app.logger.error(f"Error calculating total expenses: {str(e)}")
        return jsonify({'success': False, 'message': 'خطأ في حساب المصروفات'})


# Shipment Reports Routes
@app.route('/shipment_reports')
@login_required
@permission_required('reports')
def shipment_reports():
    """Shipment profit and loss reports page"""
    return render_template('shipment_reports.html')


@app.route('/api/shipment_reports')
@login_required
@permission_required('reports')
def api_shipment_reports():
    """API endpoint for shipment P&L reports"""
    try:
        period = request.args.get('period', 'all')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query based on period
        query = Shipment.query
        
        if period == 'today':
            today = datetime.now().date()
            query = query.filter(db.func.date(Shipment.created_at) == today)
        elif period == 'week':
            week_start = datetime.now().date() - timedelta(days=7)
            query = query.filter(db.func.date(Shipment.created_at) >= week_start)
        elif period == 'month':
            month_start = datetime.now().replace(day=1).date()
            query = query.filter(db.func.date(Shipment.created_at) >= month_start)
        elif period == 'custom' and start_date and end_date:
            query = query.filter(
                db.func.date(Shipment.created_at) >= start_date,
                db.func.date(Shipment.created_at) <= end_date
            )
        
        shipments = query.order_by(Shipment.created_at.desc()).all()
        
        # Calculate totals and build response data
        shipments_data = []
        total_revenue = 0.0
        total_expenses = 0.0
        
        for shipment in shipments:
            # Calculate distributed category expenses for this shipment
            category_expenses = shipment.calculate_category_distributed_expenses()
            direct_expenses = shipment.calculate_total_expenses()
            net_profit_with_category = shipment.calculate_net_profit_with_category_expenses()
            
            # Update shipment's linked_expenses field with category expenses
            shipment.linked_expenses = category_expenses
            
            shipment_type_ar = 'مستندات' if shipment.package_type == 'document' else 'شحنات عامة'
            
            shipments_data.append({
                'id': shipment.id,
                'tracking_number': shipment.tracking_number,
                'package_type': shipment.package_type,
                'package_type_ar': shipment_type_ar,
                'sender_name': shipment.sender_name,
                'receiver_name': shipment.receiver_name,
                'price': float(shipment.price),
                'direct_expenses': direct_expenses,
                'category_expenses': category_expenses,
                'net_profit': net_profit_with_category,
                'status': shipment.status,
                'created_at': shipment.created_at.strftime('%Y-%m-%d')
            })
            
            total_revenue += float(shipment.price)
            total_expenses += category_expenses
        
        # Commit the linked_expenses updates
        db.session.commit()
        
        summary = {
            'total_shipments': len(shipments),
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_profit': total_revenue - total_expenses
        }
        
        return jsonify({
            'success': True,
            'shipments': shipments_data,
            'summary': summary
        })
        
    except Exception as e:
        logging.error(f'Error generating shipment reports: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في تحميل التقارير: {str(e)}'})


@app.route('/api/shipment_details/<int:shipment_id>')
@login_required 
@permission_required('reports')
def api_shipment_details(shipment_id):
    """API endpoint for detailed shipment P&L analysis"""
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        
        # Get all expenses linked to this shipment
        expenses = []
        
        # Financial transactions
        financial_expenses = FinancialTransaction.query.filter_by(
            transaction_type='expense',
            shipment_id=shipment.id
        ).all()
        
        for expense in financial_expenses:
            expenses.append({
                'name': expense.name,
                'amount': float(expense.amount),
                'date': expense.transaction_date.strftime('%Y-%m-%d'),
                'type': 'مصروف شحنات عامة'
            })
        
        # General expenses
        general_expenses = ExpenseGeneral.query.filter_by(shipment_id=shipment.id).all()
        for expense in general_expenses:
            expenses.append({
                'name': expense.name,
                'amount': float(expense.amount),
                'date': expense.expense_date.strftime('%Y-%m-%d'),
                'type': 'مصروف مكتب'
            })
        
        # Document expenses
        document_expenses = ExpenseDocuments.query.filter_by(shipment_id=shipment.id).all()
        for expense in document_expenses:
            expenses.append({
                'name': expense.name,
                'amount': float(expense.amount),
                'date': expense.expense_date.strftime('%Y-%m-%d'),
                'type': 'مصروف مستندات'
            })
        
        shipment_data = {
            'tracking_number': shipment.tracking_number,
            'sender_name': shipment.sender_name,
            'receiver_name': shipment.receiver_name,
            'package_type': shipment.package_type,
            'price': float(shipment.price),
            'direct_expenses': shipment.calculate_total_expenses(),
            'category_expenses': shipment.calculate_category_distributed_expenses(),
            'net_profit': shipment.calculate_net_profit_with_category_expenses(),
            'created_at': shipment.created_at.strftime('%Y-%m-%d %H:%M'),
            'expenses': expenses
        }
        
        return jsonify({
            'success': True,
            'shipment': shipment_data
        })
        
    except Exception as e:
        logging.error(f'Error loading shipment details: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في تحميل تفاصيل الشحنة: {str(e)}'})


@app.route('/api/shipments_for_linking')
@login_required
@permission_required('expenses')
def api_shipments_for_linking():
    """API endpoint to get shipments list for expense linking"""
    try:
        # Get general shipments
        general_shipments = Shipment.query.filter(Shipment.package_type != 'document').all()
        
        # Get document shipments
        document_shipments = Shipment.query.filter(Shipment.package_type == 'document').all()
        
        shipments_data = {
            'general': [
                {
                    'id': s.id,
                    'tracking_number': s.tracking_number,
                    'sender_name': s.sender_name,
                    'receiver_name': s.receiver_name,
                    'price': float(s.price) if s.price else 0.0
                }
                for s in general_shipments
            ],
            'documents': [
                {
                    'id': s.id,
                    'tracking_number': s.tracking_number,
                    'sender_name': s.sender_name,
                    'receiver_name': s.receiver_name,
                    'price': float(s.price) if s.price else 0.0
                }
                for s in document_shipments
            ]
        }
        
        return jsonify(shipments_data)
        
    except Exception as e:
        logging.error(f'Error getting shipments for linking: {str(e)}')
        return jsonify({'error': 'Failed to get shipments list'})


@app.route('/api/general_category_expenses')
@login_required
@permission_required('expenses')
def api_general_category_expenses():
    """API endpoint to get total general category expenses"""
    try:
        total = Shipment.get_total_general_category_expenses()
        return jsonify({'total': total})
    except Exception as e:
        logging.error(f'Error getting general category expenses: {str(e)}')
        return jsonify({'total': 0.0})


@app.route('/api/document_category_expenses')
@login_required
@permission_required('expenses')
def api_document_category_expenses():
    """API endpoint to get total document category expenses"""
    try:
        total = Shipment.get_total_document_category_expenses()
        return jsonify({'total': total})
    except Exception as e:
        logging.error(f'Error getting document category expenses: {str(e)}')
        return jsonify({'total': 0.0})
    try:
        shipments = Shipment.query.order_by(Shipment.created_at.desc()).limit(50).all()
        
        shipments_data = []
        for shipment in shipments:
            shipments_data.append({
                'id': shipment.id,
                'tracking_number': shipment.tracking_number,
                'sender_name': shipment.sender_name,
                'receiver_name': shipment.receiver_name,
                'package_type': shipment.package_type,
                'price': float(shipment.price),
                'created_at': shipment.created_at.strftime('%Y-%m-%d')
            })
        
        return jsonify({
            'success': True,
            'shipments': shipments_data
        })
        
    except Exception as e:
        logging.error(f'Error loading shipments for linking: {str(e)}')
        return jsonify({'success': False, 'message': f'حدث خطأ في تحميل الشحنات: {str(e)}'})
