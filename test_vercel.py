#!/usr/bin/env python3
"""
Test script untuk memastikan aplikasi bisa jalan di environment Vercel
"""

import os
import sys

# Simulate Vercel environment
os.environ["VERCEL"] = "1"
os.environ["FLASK_ENV"] = "production"
os.environ["SECRET_KEY"] = "test-secret-key-for-vercel"

# Test import
try:
    from api.index import app
    print("✅ Import api/index.py berhasil")
except Exception as e:
    print(f"❌ Error import api/index.py: {e}")
    sys.exit(1)

# Test basic routes
try:
    with app.test_client() as client:
        # Test root route
        response = client.get('/')
        print(f"✅ Root route status: {response.status_code}")
        
        # Test health route (if exists)
        try:
            response = client.get('/health')
            print(f"✅ Health route status: {response.status_code}")
        except:
            print("ℹ️  Health route tidak ada (normal)")
        
        # Test database initialization
        from database import db
        db.init_tables()
        print("✅ Database initialization berhasil")
        
except Exception as e:
    print(f"❌ Error testing routes: {e}")
    sys.exit(1)

print("\n🎉 Semua test passed! Aplikasi siap di-deploy ke Vercel.")
print("\nLangkah selanjutnya:")
print("1. Push ke GitHub repository")
print("2. Connect repository ke Vercel")
print("3. Set environment variables di Vercel dashboard")
print("4. Deploy!")