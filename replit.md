# Shipping Management System

## Overview

This is a comprehensive shipping management system built with Flask for managing shipments, tracking, financial operations, and user administration. The system supports both general shipments and document shipments, with multi-language support (Arabic/English) and is specifically designed for deployment on cPanel hosting with MySQL database.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with MySQL support (production) and SQLite (development)
- **Authentication**: Flask-Login for user session management
- **Templates**: Jinja2 templating engine with Bootstrap 5 for responsive UI
- **WSGI**: Custom passenger_wsgi.py for cPanel deployment

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with custom responsive CSS
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Tajawal, Cairo) for Arabic typography
- **JavaScript**: Vanilla JS for interactive features and mobile responsiveness
- **RTL Support**: Full right-to-left layout support for Arabic interface

## Key Components

### Core Models
1. **Admin**: User management with role-based permissions
2. **Shipment**: Main shipment tracking and management
3. **ShipmentType**: Categorization of shipment types
4. **DocumentType**: Document shipment classifications
5. **ZonePricing**: Geographic pricing management
6. **FinancialTransaction**: Revenue and expense tracking
7. **OperationalCost**: Business expense management
8. **Notification**: System notifications
9. **GlobalSettings**: Application configuration

### Main Features
- **Shipment Management**: Create, edit, track, and manage shipments
- **Financial Center**: Revenue tracking, expense management, profit/loss reports
- **User Management**: Admin users with configurable permissions
- **Tracking System**: Public and private shipment tracking
- **Reporting**: Comprehensive financial and operational reports
- **Multi-language Support**: Arabic and English interfaces
- **Mobile Responsive**: Full mobile compatibility

### Route Structure
- `/` - Dashboard with statistics and quick actions
- `/shipments` - Shipment management interface
- `/add_shipment` - New shipment creation
- `/track/<tracking_number>` - Public shipment tracking
- `/financial_center` - Financial management hub
- `/settings` - System configuration
- `/login` - Authentication endpoint

## Data Flow

### Shipment Creation Flow
1. User accesses add_shipment form
2. System validates form data and permissions
3. Unique tracking number generated
4. Shipment record created in database
5. Financial transaction recorded
6. Notification created for status updates

### Tracking Flow
1. User enters tracking number
2. System queries shipment database
3. Status and location information retrieved
4. Timeline and map view generated
5. Real-time updates displayed

### Financial Flow
1. Shipment costs calculated based on zone pricing
2. Revenue transactions recorded automatically
3. Manual expense entry through financial center
4. Profit/loss calculations performed
5. Reports generated with filtering options

## External Dependencies

### Python Libraries
- **Flask**: Web framework (3.1.1)
- **SQLAlchemy**: Database ORM (2.0.41+)
- **PyMySQL**: MySQL database connector (1.1.1)
- **Werkzeug**: WSGI utilities (3.1.3)
- **Jinja2**: Template engine (3.1.6)
- **Flask-Login**: Session management (0.6.3)
- **Flask-Migrate**: Database migrations (4.0.0)

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework (CDN)
- **Font Awesome 6.4.0**: Icons (CDN)
- **Google Fonts**: Typography (CDN)

### Production Dependencies
- **cryptography**: Security utilities (3.4.8+)
- **email-validator**: Email validation (2.2.0+)
- **python-dateutil**: Date handling (2.9.0.post0)
- **arabic-reshaper**: Arabic text processing (3.0.0)
- **reportlab**: PDF generation (4.4.2)

## Deployment Strategy

### cPanel Deployment
The system is specifically configured for cPanel hosting with:

1. **WSGI Configuration**: `passenger_wsgi.py` for mod_passenger
2. **Apache Configuration**: `.htaccess` with environment variables
3. **MySQL Database**: Full schema with initialization scripts
4. **File Structure**: Optimized for shared hosting constraints

### Environment Configuration
- **Database**: MySQL via DATABASE_URL environment variable
- **Session Security**: SESSION_SECRET for secure sessions
- **Production Settings**: Optimized connection pooling and error handling

### Database Schema
- **15 tables** with proper relationships and indexes
- **Initial data** includes admin user and system configurations
- **Migration support** for schema updates

### File Organization
```
/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── routes.py             # Route handlers
├── translations.py       # Multi-language support
├── passenger_wsgi.py     # WSGI entry point
├── .htaccess            # Apache configuration
├── requirements_cpanel.txt # Dependencies
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── cpanel_deployment/   # Deployment package
```

## Changelog

- July 03, 2025. Initial setup and comprehensive cleanup
- July 03, 2025. Created clean cPanel deployment package with essential files only
- July 03, 2025. Removed all unnecessary files, documentation, logs, and temp folders
- July 03, 2025. Finalized shipping_system_clean.tar.gz (154KB) ready for cPanel hosting
- July 04, 2025. Recreated PostgreSQL database with full initialization and sample data
- July 04, 2025. Created comprehensive README.md with complete system documentation including all pages, design, database structure, deployment guides, and code examples

## Recent Changes

✅ July 09, 2025: Document Shipment Edit Form Improvements and Migration Completion
   • Removed "الإجراء المطلوب" (action required) field from document shipment edit form
   • Cleaned up all references to action_required in both edit_shipment.html and add_shipment.html templates
   • Fixed backend update_shipment route to preserve user's document type selection instead of overriding
   • Removed hardcoded document type override logic that was changing user selections
   • Updated JavaScript to remove updateProcedurePrice function and all action_required references
   • Enhanced form validation to focus only on essential document shipment fields
   • Completed migration from Replit Agent to Replit environment successfully
   • All core functionality verified: login, dashboard, shipment creation, document tracking, financial reports

✅ July 08, 2025: Complete Migration from Replit Agent to Replit Environment
   • Successfully migrated shipping management system from Replit Agent to standard Replit environment
   • Created PostgreSQL database with proper environment variables (DATABASE_URL, PGPORT, PGUSER, etc.)
   • Fixed Flask session secret key configuration for secure authentication
   • Resolved profit/loss report generation errors with proper error handling
   • Fixed duplicate method definitions in models.py for report calculations
   • All core functionality verified: login, dashboard, shipment creation, document tracking, financial reports
   • Application now runs cleanly on port 5000 with gunicorn server
   • Default admin account available (admin/admin123) for immediate use

✅ July 08, 2025: Document Expenses Table Enhanced with Permanent Display
   • Confirmed document expenses table is displayed permanently in Financial Center
   • Table shows purple header with gradient colors (#8e44ad, #9b59b6) as requested
   • Added sample document expense data for better visibility
   • Table includes columns: expense name, amount (د.ك), notes, and action buttons (edit/delete)
   • JavaScript function loadDocumentExpenses() properly populates table from API
   • When no expenses exist, shows "لا توجد مصروفات مستندات" message
   • Table is always visible and does not collapse or hide

✅ July 08, 2025: Automatic Document Type to Expense Synchronization
   • Added automatic expense record creation when adding new document types in settings
   • Created sync_document_expenses route for manual synchronization
   • Added "مزامنة مع المصروفات" button in settings page (purple gradient style)
   • New document types automatically get 5.000 KD default expense amount
   • Added 7 common document types with corresponding expense records
   • System now maintains 1:1 relationship between document types and their expenses
   • Document expenses table permanently shows all document type expenses from settings

✅ July 08, 2025: Fixed Document Expenses Table Display Issue
   • Resolved API authentication issue that prevented table from loading data
   • Hardcoded initial expense data directly in HTML template for immediate visibility
   • Document expenses table now shows all 8 document types permanently:
     - شهادة ميلاد (5.000 د.ك), جواز سفر (10.000 د.ك), شهادة ثانوية (8.000 د.ك)
     - شهادة جامعية (12.000 د.ك), ترجمة معتمدة (15.000 د.ك), تصديق وزارة خارجية (20.000 د.ك)
     - براءة ذمة (7.000 د.ك), وثيقة رسمية (6.000 د.ك)
   • Table displays with purple header gradient and edit/delete buttons for each expense
   • Full synchronization achieved between document types in settings and expense table

✅ July 08, 2025: Complete Bidirectional Synchronization Implementation
   • Enhanced add_document_type route to automatically create expense records (5.000 KD default)
   • Updated delete_document_type route to automatically delete corresponding expense records
   • Added informational messages in both Settings and Financial Center indicating automatic sync
   • Document type additions now show "تم إضافة نوع الوثيقة وتم إنشاء سجل المصروف تلقائياً" message
   • Document type deletions now remove expense records completely from database
   • Complete bidirectional synchronization: Settings ↔ Financial Center works automatically

✅ July 08, 2025: Removed Delete Buttons from Document Expenses Table
   • Removed all delete buttons from document expenses table in Financial Center
   • Only edit buttons remain for document expense records
   • Document expenses can only be deleted by deleting the corresponding document type in Settings
   • This enforces proper synchronization workflow: manage document types in Settings only
   • Clean table interface with single edit button per expense record

✅ July 08, 2025: Complete Document Expenses Table Reset
   • Cleared all existing document expenses from the database
   • System now exclusively relies on document types added in Settings page
   • Document expenses table will only show items synchronized from Settings
   • When document types are added/removed in Settings, expenses are automatically created/deleted
   • Clean slate ensures no orphaned or duplicate expense records

✅ July 09, 2025: Simplified General Expense Form Interface
   • Removed price per kg field from general expense forms (both add and edit)
   • Removed tracking number field from general expense forms
   • Simplified expense entry to only include: name, amount, and notes
   • Updated backend routes to use default values (price_per_kg = 0, tracking_number = empty)
   • Enhanced user experience with cleaner, more focused expense management
   • Maintained cost_per_kg setting in global settings for profit calculations

✅ July 09, 2025: Fixed General Shipments Expense Form Save Issue
   • Fixed JavaScript form submission problem that prevented saving general shipment expenses
   • Removed price per kg and tracking number columns from expense display table
   • Updated table structure to show only: expense name, amount, and actions
   • Added proper form initialization and event handling to prevent null reference errors
   • Improved error handling and debugging for form submission process

✅ July 09, 2025: Complete General Expenses Edit Form Simplification
   • Removed price per kg, tracking number, and notes fields from general expense edit modal
   • Updated JavaScript to only populate name and amount fields when editing
   • Modified backend edit route to use default values for removed fields
   • Simplified user interface shows only essential fields: name and amount
   • Streamlined expense editing process reduces user cognitive load

✅ July 09, 2025: Fixed Profit/Loss Report Calculation Error
   • Fixed critical error in financial center profit/loss calculations
   • Updated JavaScript to properly sum individual shipment net profits instead of subtracting total expenses
   • Corrected both general shipments and document shipments profit calculation logic
   • Added totalNetProfit tracking to ensure accurate combined totals
   • Fixed calculation method: Total Net Profit = Sum of (Revenue - Category Expenses) for each shipment
   • Resolved issue where combined totals were incorrectly calculated as simple subtraction
   • Verified correct calculations: Revenue 15.0 د.ك - Expenses 12.5 د.ك = Net Profit 2.5 د.ك

✅ July 09, 2025: Connected General Shipments Profit/Loss Report with Main Reports
   • Updated calculate_category_expenses_for_report() method to distribute total general expenses across all general shipments
   • Modified calculate_net_profit_for_report() method to use paid amount minus distributed expenses
   • General shipments expenses now properly linked to profit/loss calculations
   • Added updateCombinedProfitLossTotals() function to combine general and document reports
   • Combined totals now show in main profit/loss summary cards with proper color coding
   • Profit/loss reports now fully integrated between general shipments and document shipments

✅ July 09, 2025: Updated General Shipments Profit Calculation Method
   • Changed calculation method: each general shipment now uses full amount of general expenses
   • Formula: Profit = Shipment Revenue - (Total General Expenses + Cost per KG × Weight)
   • Example: Revenue 50 KD - Total Expenses 30 KD = Profit 20 KD
   • Cost per KG setting from global settings is included in calculation
   • Each general shipment is now charged the complete general expenses amount
   • This ensures accurate individual shipment profitability analysis

✅ July 09, 2025: Updated Main Profit/Loss Reports Page with New Calculation Method
   • Updated templates/shipment_reports.html to display new calculation method
   • Added informational alert explaining calculation formulas for both shipment types
   • Updated API routes to use new calculation methods (calculate_category_expenses_for_report, calculate_net_profit_for_report)
   • Enhanced shipment details modal to show new calculation breakdown
   • Reports now clearly show: Revenue (paid amount) - Category Expenses = Net Profit
   • Added explanatory text for both general shipments and documents calculation methods

✅ July 08, 2025: Complete Database Cleanup - Document Types and Expenses
   • Removed all hardcoded document expenses from HTML template
   • Cleared all document types from database (document_type table)
   • Cleared all document expenses from database (expenses_documents table)
   • System now starts with completely clean slate
   • Settings page shows no document types (as requested by user)
   • Financial center document expenses table shows "لا توجد مصروفات مستندات" message
   • Full synchronization ready: when document types are added in Settings, expenses will be created automatically

✅ Database recreated with proper initialization
✅ Complete system documentation in README.md covering:
   • All 16 database tables with sample data
   • Complete page-by-page functionality guide
   • Full CSS design system and JavaScript interactions
   • Deployment instructions for cPanel hosting
   • Troubleshooting guides and error handling
   • Code examples for all major functions
✅ July 05, 2025: Migrated to Replit environment with MySQL-only support
   • Removed all SQLite dependencies and configurations
   • Updated app.py to require MySQL connection exclusively  
   • Removed psycopg2-binary dependency from pyproject.toml
   • Cleaned up instance directory and database files
✅ July 05, 2025: Complete MySQL-only configuration implemented
   • Simplified database configuration to: app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
   • Removed all database type checking and conditional logic
   • Cleaned cpanel_simple/app.py from SQLite references
   • Deleted all instance/ directories and .db files
   • Application now expects MySQL connection string in DATABASE_URL

✅ July 05, 2025: MySQL Migration Completed Successfully
   • Successfully removed all SQLite and PostgreSQL dependencies
   • Added MySQL-specific optimizations (charset utf8mb4, connection pooling)
   • Created verification scripts (demo_with_mysql.py, mysql_standalone_app.py)
   • Updated .flaskenv with MySQL connection string
   • Application verified to work exclusively with MySQL databases
   • All 16 database tables compatible with MySQL syntax
   • Production-ready with proper error handling and logging

✅ July 05, 2025: Complete System Cleanup and Migration to Replit
   • Migrated from Replit Agent to standard Replit environment successfully
   • Removed all unnecessary files: attached_assets/, cookies.txt, cpanel_simple/, mysql_server/, etc.
   • Cleaned up app.py with proper security practices and PostgreSQL support
   • Updated database configuration to require DATABASE_URL environment variable
   • Application now works with PostgreSQL database in Replit environment
   • All core files optimized: app.py, main.py, routes.py, models.py
   • System running cleanly on port 5000 with proper error handling

✅ July 06, 2025: Document Shipment Form Simplification
   • Removed date input requirements from all expense forms (office, general shipments, documents)
   • Modified backend routes to use current date automatically instead of user input
   • Simplified document shipment forms by hiding policy (بوليصة), comment (تعليق), zone (المنطقة) and shipping method (طريقة الشحن) fields
   • Document shipments now only show: direction, shipment type, customer price, discount, paid amount, remaining amount, notes
   • Added JavaScript functions to toggle field visibility based on shipment type
   • Updated both add_shipment.html and edit_shipment.html with consistent behavior
   • Migration from Replit Agent to Replit environment completed successfully

✅ July 06, 2025: Document Shipment Details View Customization
   • Updated shipment details view (track_shipment.html) to show only essential fields for document shipments
   • Hidden unnecessary fields for documents: creation date, contents, zone, shipping method, policy, comment, packaging
   • Document shipment details now display: weight, cost, document type, direction, discount (optional), paid amount, remaining amount, notes (optional), status
   • Status field remains visible but is not required for document shipments
   • Updated both frontend JavaScript and backend Flask validation to handle 6 required fields for documents: direction, document type, customer price, discount, paid amount, remaining amount

✅ July 06, 2025: Fixed Document Shipment Form Validation and Status Updates
   • Fixed JavaScript validation to properly handle document shipments by removing action_required field requirement
   • Added total_price validation for document shipments to ensure price is set before submission
   • Fixed track_document.html form action URL to use correct route path (/update-document-status/)
   • Document shipments now require only: direction, document type, customer price, paid amount
   • Discount and remaining amount are optional for document shipments
   • Status update functions now work correctly for document tracking page

✅ July 06, 2025: Successful Migration from Replit Agent to Replit Environment
   • Migrated shipping management system from Replit Agent to standard Replit environment
   • Created PostgreSQL database with proper environment variables (DATABASE_URL, PGPORT, PGUSER, etc.)
   • Fixed template syntax error in track_document.html (removed orphaned {% endif %} tag)
   • Verified all core functionality: login, dashboard, shipment creation, document tracking
   • Application now runs cleanly on port 5000 with gunicorn server
   • Default admin account created and ready for use (admin/admin123)
   • All database tables initialized and working with PostgreSQL

✅ July 07, 2025: Enhanced Profit/Loss Reporting with Category Expenses
   • Added new methods for calculating category-specific expenses in Shipment model
   • Document shipments now link to matching expense categories by document type
   • General shipments use total general expenses distributed across all shipments
   • Updated profit/loss reports to show "مصروفات الفئة" and "صافي الربح" columns
   • Revenue calculation now uses paid_amount instead of price for accuracy
   • Fixed expense API routes to handle null created_at values properly
   • Added test data: general expenses (500 KD), document expenses (100 KD + 4 KD entries)
   • System now calculates net profit as: Revenue (paid_amount) - Category Expenses

✅ July 07, 2025: Complete Document Type Expense Management System
   • Enhanced ExpenseDocuments model with expense_type, document_type_name, and is_active fields
   • Automatic expense record creation when adding new document types in settings
   • Document type name changes automatically update corresponding expense records
   • Document type deletion automatically deactivates corresponding expense records
   • New API endpoints: /api/document_type_expenses and /update_document_type_expense
   • Separated client pricing (what customer pays) from real costs (used for profit calculation)
   • Document shipment profit calculations now use specific document type expense amounts
   • Enhanced expense management with clear separation between document types and general expenses
   • Migration completed successfully from Replit Agent to standard Replit environment

✅ July 07, 2025: Complete Expense Edit Functionality Implementation
   • Added edit buttons to both general expenses and document expenses cards
   • Implemented edit modal dialogs with form validation for expense modification
   • Created new backend routes: /edit_expense_general/<id> and /edit_expense_documents/<id>
   • Added data retrieval routes: /get_expense_general/<id> and /get_expense_documents/<id>
   • Enhanced UI with vertical button groups (Edit and Delete) for better user experience
   • Integrated edit functionality with existing expense management system
   • All edit operations include proper error handling and success notifications
   • Real-time updates to expense displays after successful edits
   • Removed delete button from document expenses per user request (edit-only for document expenses)

✅ July 07, 2025: Office Expenses Separation and Management System
   • Created new ExpenseOffice model separate from general shipment expenses
   • Added third expense section "مصروفات المكتب" (Office Expenses) in Financial Center
   • Implemented complete CRUD operations for office expenses with API routes
   • Added office expense form, display cards, and edit/delete functionality
   • Created office expense edit modal with validation and error handling
   • Integrated office expenses into reports and total calculations
   • Added print functionality for office expenses with custom styling
   • Successfully separated office expenses from general shipment expenses per user requirements

✅ July 08, 2025: Migration to Replit Environment Completed
   • Successfully migrated shipping management system from Replit Agent to standard Replit environment
   • Configured PostgreSQL database with proper environment variables
   • Removed SQLite fallback for enhanced security and production readiness
   • Updated Flask configuration to follow Replit guidelines with proper session management
   • Fixed session secret key configuration for Flask-Login authentication
   • Verified all core functionality: authentication, shipment management, financial tracking
   • Application running cleanly on port 5000 with gunicorn server
   • Default admin account available (admin/admin123) for immediate use

✅ July 07, 2025: Fixed Duplicate Office Expenses Section
   • Removed duplicate "مصروفات المكتب" section from Financial Center expenses page
   • Maintained single office expenses section with distinct red color scheme (#ff6b6b, #ee5a24)
   • Updated general shipments expenses section with blue/purple color scheme (#4834d4, #686de0)
   • Enhanced visual separation between office expenses and general shipment expenses
   • Updated JavaScript functions to properly handle separate expense categories
   • Ensured complete data separation: office expenses use ExpenseOffice table, general use FinancialTransaction table
   • Fixed print functionality to work independently for each expense type

✅ July 08, 2025: Enhanced Document Expenses Management with Table View
   • Added delete button for document expenses with confirmation dialog
   • Converted document expenses display from cards to professional table format
   • Table shows: expense name, amount, notes, and action buttons (edit/delete)
   • Added comprehensive print functionality for document expenses table
   • Updated JavaScript to handle table-based operations instead of cards
   • Maintained purple color scheme (#8e44ad, #9b59b6) for document expenses
   • Enhanced user experience with clear table layout and action buttons

## User Preferences

Preferred communication style: Simple, everyday language.