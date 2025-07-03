#!/usr/bin/env python3
"""
Test script to verify deployment setup
Run this to check if everything is configured correctly
"""

import sys
import os

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 اختبار إصدار Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - متوافق")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - غير متوافق (يحتاج 3.8+)")
        return False

def test_required_modules():
    """Test if required Python modules are available"""
    print("\n📦 اختبار المكتبات المطلوبة...")
    
    required_modules = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'sqlalchemy',
        'pymysql',
        'werkzeug',
        'jinja2'
    ]
    
    all_good = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - غير مثبت")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 اختبار بنية الملفات...")
    
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
    
    required_dirs = [
        'templates',
        'static',
        'instance'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} - مفقود")
            all_good = False
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            file_count = len(os.listdir(dir_name))
            print(f"✅ {dir_name}/ ({file_count} ملف)")
        else:
            print(f"❌ {dir_name}/ - مفقود")
            all_good = False
    
    return all_good

def test_app_import():
    """Test if Flask app can be imported"""
    print("\n🚀 اختبار استيراد التطبيق...")
    
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from app import app
        print("✅ تم استيراد Flask app بنجاح")
        
        # Test app configuration
        with app.app_context():
            print("✅ تم تهيئة context بنجاح")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False

def test_database_config():
    """Test database configuration"""
    print("\n💾 اختبار تكوين قاعدة البيانات...")
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if 'mysql+pymysql://' in database_url:
            print("✅ DATABASE_URL مكون لـ MySQL")
            
            # Parse URL to check components
            if 'your_password' in database_url or 'your_user' in database_url:
                print("⚠️ تحذير: يجب تحديث معلومات قاعدة البيانات الحقيقية")
                return False
            else:
                print("✅ معلومات قاعدة البيانات محدثة")
                return True
        else:
            print(f"⚠️ تحذير: DATABASE_URL غير مكون لـ MySQL: {database_url}")
            return False
    else:
        print("❌ DATABASE_URL غير مكون")
        return False

def generate_report():
    """Generate comprehensive test report"""
    print("=" * 60)
    print("🔍 تقرير فحص نشر نظام إدارة الشحن")
    print("=" * 60)
    
    tests = [
        ("إصدار Python", test_python_version),
        ("المكتبات المطلوبة", test_required_modules),
        ("بنية الملفات", test_file_structure),
        ("استيراد التطبيق", test_app_import),
        ("تكوين قاعدة البيانات", test_database_config)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 ملخص النتائج:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ نجح" if result else "❌ فشل"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nالنتيجة: {passed}/{total} اختبارات نجحت")
    
    if passed == total:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للنشر")
        print("\nالخطوات التالية:")
        print("1. ارفع الملفات إلى cPanel")
        print("2. حدث معلومات قاعدة البيانات في .htaccess")
        print("3. ثبت المكتبات: pip install -r requirements_cpanel.txt")
        print("4. زر الموقع واختبر النظام")
    else:
        print(f"\n⚠️ {total - passed} اختبارات فشلت. يرجى حل المشاكل قبل النشر")
        print("\nراجع التفاصيل أعلاه لحل المشاكل")

if __name__ == "__main__":
    generate_report()