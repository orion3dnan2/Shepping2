#!/usr/bin/env python3
"""
اختبار اتصال قاعدة البيانات PostgreSQL لـ Render
"""
import os
import psycopg2
from urllib.parse import urlparse

def test_database_connection():
    """اختبار الاتصال بقاعدة البيانات"""
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL غير موجود في متغيرات البيئة")
        return False
    
    # تحليل رابط قاعدة البيانات
    try:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        parsed = urlparse(database_url)
        print(f"🔍 اختبار الاتصال بـ: {parsed.hostname}:{parsed.port}")
        print(f"📁 قاعدة البيانات: {parsed.path[1:]}")
        print(f"👤 المستخدم: {parsed.username}")
        
        # محاولة الاتصال
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # اختبار استعلام بسيط
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ اتصال ناجح! إصدار PostgreSQL: {version[0][:50]}...")
        
        # اختبار إنشاء جدول
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                message TEXT
            );
        """)
        
        cursor.execute("INSERT INTO test_table (message) VALUES ('Test connection successful');")
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM test_table;")
        count = cursor.fetchone()
        print(f"📊 عدد السجلات في جدول الاختبار: {count[0]}")
        
        # تنظيف
        cursor.execute("DROP TABLE test_table;")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("🎉 اختبار قاعدة البيانات مكتمل بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ فشل اختبار قاعدة البيانات: {str(e)}")
        print(f"🔧 نوع الخطأ: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 بدء اختبار اتصال قاعدة البيانات...")
    test_database_connection()