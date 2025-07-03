#!/usr/bin/env python3
"""
cPanel Deployment Script for Shipping Management System
This script helps deploy the system on cPanel hosting with MySQL database
"""

import os
import sys
from pathlib import Path
import shutil

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'main.py', 
        'models.py',
        'routes.py',
        'translations.py',
        'passenger_wsgi.py',
        '.htaccess',
        'requirements_cpanel.txt',
        'database_schema.sql'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ الملفات الناقصة:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ جميع الملفات الأساسية موجودة")
    return True

def create_deployment_package():
    """Create a deployment package with all necessary files"""
    print("📦 إنشاء حزمة التثبيت...")
    
    # Create deployment directory
    deploy_dir = "cpanel_deployment"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Essential files to copy
    essential_files = [
        'app.py',
        'main.py',
        'models.py', 
        'routes.py',
        'translations.py',
        'passenger_wsgi.py',
        '.htaccess',
        'requirements_cpanel.txt',
        'database_schema.sql',
        'setup_mysql.py'
    ]
    
    # Copy essential files
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"✅ تم نسخ {file}")
    
    # Copy directories
    dirs_to_copy = ['templates', 'static']
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(deploy_dir, dir_name))
            print(f"✅ تم نسخ مجلد {dir_name}")
    
    # Create instance directory
    instance_dir = os.path.join(deploy_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    # Create deployment instructions
    instructions = """
# تعليمات التثبيت على cPanel

## 1. رفع الملفات
- ارفع جميع الملفات إلى مجلد public_html/shipping/
- تأكد من أن الأذونات صحيحة (644 للملفات، 755 للمجلدات)

## 2. إعداد قاعدة البيانات
- أنشئ قاعدة بيانات MySQL جديدة
- استورد ملف database_schema.sql
- حدث معلومات الاتصال في .htaccess

## 3. تكوين البيئة
- حدت مسار Python في .htaccess
- قم بتثبيت المكتبات: pip install -r requirements_cpanel.txt
- شغل: python3 setup_mysql.py

## 4. اختبار النظام
- زر: https://yourdomain.com/shipping/
- سجل دخول: admin / admin123
"""
    
    with open(os.path.join(deploy_dir, 'INSTALLATION_INSTRUCTIONS.md'), 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ تم إنشاء حزمة التثبيت في مجلد: {deploy_dir}")
    return deploy_dir

def validate_database_schema():
    """Validate the database schema file"""
    schema_file = 'database_schema.sql'
    if not os.path.exists(schema_file):
        print("❌ ملف database_schema.sql غير موجود")
        return False
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for essential tables
    essential_tables = ['admin', 'shipment', 'shipment_type', 'document_type']
    for table in essential_tables:
        if f'CREATE TABLE {table}' not in content:
            print(f"❌ جدول {table} غير موجود في ملف قاعدة البيانات")
            return False
    
    print("✅ ملف قاعدة البيانات صحيح")
    return True

def check_htaccess_config():
    """Check .htaccess configuration"""
    print("🔍 فحص تكوين .htaccess...")
    
    if not os.path.exists('.htaccess'):
        print("❌ ملف .htaccess غير موجود")
        return False
    
    with open('.htaccess', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for essential configurations
    required_configs = [
        'DATABASE_URL',
        'SESSION_SECRET',
        'PassengerPython',
        'passenger_wsgi.py'
    ]
    
    missing_configs = []
    for config in required_configs:
        if config not in content:
            missing_configs.append(config)
    
    if missing_configs:
        print("❌ إعدادات ناقصة في .htaccess:")
        for config in missing_configs:
            print(f"   - {config}")
        return False
    
    print("✅ تكوين .htaccess صحيح")
    return True

def main():
    """Main deployment function"""
    print("🚀 بدء عملية التحضير للنشر على cPanel")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ يرجى التأكد من وجود جميع الملفات المطلوبة")
        return False
    
    # Validate database schema
    if not validate_database_schema():
        print("\n❌ مشكلة في ملف قاعدة البيانات")
        return False
    
    # Create deployment package
    deploy_dir = create_deployment_package()
    
    # Check .htaccess configuration
    if not check_htaccess_config():
        print("\n❌ مشكلة في إعدادات .htaccess")
        return False
    
    print("\n🎉 النظام جاهز للنشر!")
    print(f"📁 حزمة التثبيت: {deploy_dir}")
    print("\n📋 الخطوات التالية:")
    print("1. ارفع محتويات مجلد cpanel_deployment إلى cPanel")
    print("2. أنشئ قاعدة بيانات MySQL واستورد database_schema.sql")
    print("3. حدث معلومات الاتصال في .htaccess")
    print("4. ثبت المكتبات وشغل setup_mysql.py")
    
    return True

if __name__ == "__main__":
    main()