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

## User Preferences

Preferred communication style: Simple, everyday language.