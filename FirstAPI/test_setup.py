"""
Test script to verify the FastAPI application setup
"""

import sys
import os

print("=" * 60)
print("🧪 FastAPI Todo Application - System Check")
print("=" * 60)

# Test 1: Check Python version
print("\n1️⃣ Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"   ❌ Python version too old. Need 3.8+")
    sys.exit(1)

# Test 2: Check required modules
print("\n2️⃣ Checking required modules...")
required_modules = {
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'pymongo': 'PyMongo',
    'pydantic': 'Pydantic',
    'jinja2': 'Jinja2',
    'bson': 'BSON'
}

missing_modules = []
for module, name in required_modules.items():
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} - NOT INSTALLED")
        missing_modules.append(name)

if missing_modules:
    print(f"\n   ⚠️  Missing modules: {', '.join(missing_modules)}")
    print("   Run: pip install -r requirements.txt")
else:
    print("\n   ✅ All required modules installed!")

# Test 3: Check database connection
print("\n3️⃣ Checking database connection...")
try:
    from database import db, todos_collection, check_connection
    if db is not None:
        if check_connection():
            print("   ✅ MongoDB connected successfully!")
            print(f"   📦 Database: {db.name}")
            if todos_collection is not None:
                count = todos_collection.count_documents({})
                print(f"   📝 Current todos in database: {count}")
        else:
            print("   ⚠️  Database connection exists but ping failed")
    else:
        print("   ⚠️  Database not connected - will use in-memory storage")
except Exception as e:
    print(f"   ⚠️  Database connection issue: {e}")
    print("   Application will run with in-memory storage")

# Test 4: Check file structure
print("\n4️⃣ Checking file structure...")
required_files = [
    'main.py',
    'database.py',
    'requirements.txt',
    'static/css/style.css',
    'static/js/script.js',
    'templates/index.html',
    'templates/todos.html',
    'templates/item.html'
]

for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING")

# Test 5: Try importing main application
print("\n5️⃣ Testing application import...")
try:
    from main import app, DB_CONNECTED
    print(f"   ✅ FastAPI application imported successfully!")
    print(f"   📊 Database status: {'Connected' if DB_CONNECTED else 'In-memory mode'}")
except Exception as e:
    print(f"   ❌ Failed to import application: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
if not missing_modules and os.path.exists('main.py'):
    print("✅ System is ready to run!")
    print("\n🚀 To start the application, run:")
    print("   python main.py")
    print("\nOr:")
    print("   uvicorn main:app --reload")
    print("\n🌐 Access at: http://127.0.0.1:8000")
else:
    print("⚠️  Some issues found. Please fix them before running.")

print("=" * 60)

