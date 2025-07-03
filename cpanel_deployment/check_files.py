#!/usr/bin/env python3
"""
Quick file checker for cPanel deployment
Run this script to verify all files are in place
"""

import os
from pathlib import Path

def check_deployment_files():
    """Check if all necessary files exist"""
    print("🔍 فحص ملفات النشر...")
    print("=" * 40)
    
    # Core Python files
    core_files = {
        'app.py': 'ملف التطبيق الرئيسي',
        'main.py': 'نقطة الدخول',
        'models.py': 'نماذج قاعدة البيانات',
        'routes.py': 'مسارات التطبيق',
        'translations.py': 'ملف الترجمة',
        'passenger_wsgi.py': 'ملف WSGI للاستضافة'
    }
    
    # Configuration files
    config_files = {
        '.htaccess': 'إعدادات Apache',
        'requirements_cpanel.txt': 'مكتبات Python المطلوبة',
        'database_schema.sql': 'مخطط قاعدة البيانات',
        'setup_mysql.py': 'سكريبت إعداد MySQL'
    }
    
    # Directories
    required_dirs = {
        'templates': 'قوالب HTML',
        'static': 'ملفات CSS وJS والصور',
        'instance': 'مجلد البيانات'
    }
    
    # Check core files
    print("📄 الملفات الأساسية:")
    all_good = True
    
    for file, desc in core_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes) - {desc}")
        else:
            print(f"❌ {file} - {desc}")
            all_good = False
    
    print("\n⚙️ ملفات التكوين:")
    for file, desc in config_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes) - {desc}")
        else:
            print(f"❌ {file} - {desc}")
            all_good = False
    
    print("\n📁 المجلدات:")
    for dir_name, desc in required_dirs.items():
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            file_count = len([f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))])
            print(f"✅ {dir_name}/ ({file_count} ملف) - {desc}")
        else:
            print(f"❌ {dir_name}/ - {desc}")
            all_good = False
    
    # Check templates specifically
    if os.path.exists('templates'):
        essential_templates = [
            'base.html', 'login.html', 'dashboard.html', 
            'add_shipment.html', 'shipments.html'
        ]
        
        print("\n🖼️ القوالب الأساسية:")
        for template in essential_templates:
            template_path = os.path.join('templates', template)
            if os.path.exists(template_path):
                print(f"✅ {template}")
            else:
                print(f"❌ {template}")
                all_good = False
    
    print("\n" + "=" * 40)
    
    if all_good:
        print("🎉 جميع الملفات موجودة والنظام جاهز للنشر!")
        print("\n📋 الخطوات التالية:")
        print("1. ارفع هذا المجلد إلى public_html/shipping/ في cPanel")
        print("2. أنشئ قاعدة بيانات MySQL")
        print("3. استورد database_schema.sql")
        print("4. حدث .htaccess بمعلومات قاعدة البيانات")
        print("5. ثبت المكتبات: pip install -r requirements_cpanel.txt")
        print("6. شغل: python3 setup_mysql.py")
        print("7. زر موقعك واختبر النظام")
    else:
        print("❌ يوجد ملفات ناقصة! يرجى التأكد من اكتمال التثبيت")
    
    return all_good

if __name__ == "__main__":
    check_deployment_files()