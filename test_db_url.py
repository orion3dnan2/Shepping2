#!/usr/bin/env python3
"""
اختبار رابط قاعدة البيانات الجديد
"""
import psycopg2
from urllib.parse import urlparse

# الرابط الجديد
DATABASE_URL = "postgresql://shipments_user:nbFq48a7W4Qv376fXLChL7Wenrh4TIgR@dpg-d1hm7pvfte5s73adkpp0-a.oregon-postgres.render.com/shipments_z1dk"

def test_connection():
    """اختبار الاتصال بالرابط الجديد"""
    try:
        print("🔍 اختبار الرابط الجديد...")
        parsed = urlparse(DATABASE_URL)
        print(f"Host: {parsed.hostname}")
        print(f"Port: {parsed.port}")
        print(f"Database: {parsed.path[1:]}")
        print(f"User: {parsed.username}")
        
        # اختبار الاتصال
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ اتصال ناجح!")
        print(f"PostgreSQL Version: {version[0][:80]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ فشل الاتصال: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()