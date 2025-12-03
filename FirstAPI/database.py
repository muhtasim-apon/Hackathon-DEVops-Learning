from pymongo import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
import os

# Your MongoDB credentials
username = "syedmuhtasimapon_db_user"  # Replace with your MongoDB username
password = "apon2gmail.com"  # Replace with your MongoDB password

# URL encode the password (important for special characters)
escaped_password = urllib.parse.quote_plus(password)
escaped_username = urllib.parse.quote_plus(username)

# Connection string with proper SSL settings
MONGODB_URI = f"mongodb+srv://{escaped_username}:{escaped_password}@firstapi.selxbpc.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"

# Initialize variables
db = None
todos_collection = None
client = None

# Create MongoDB client
try:
    client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi('1'),
        tls=True,
        tlsAllowInvalidCertificates=True,  # For development only
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        connectTimeoutMS=5000
    )

    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connected successfully!")

    # Get database and collection
    db = client['hackathon_db']  # Your database name
    todos_collection = db['todos']  # Collection for todos

    # Create indexes for better performance
    todos_collection.create_index([("created_at", -1)])
    todos_collection.create_index([("completed", 1)])
    todos_collection.create_index([("priority", 1)])

    print(f"✅ Database: {db.name}")
    print(f"✅ Collection: todos")

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("⚠️ Application will run with in-memory storage")
    db = None
    todos_collection = None


# Helper function to check database connection
def check_connection():
    """Check if database connection is active"""
    if client is None or db is None:
        return False
    try:
        client.admin.command('ping')
        return True
    except Exception:
        return False


# Helper function to get database info
def get_db_info():
    """Get database connection information"""
    if db is None:
        return {
            "connected": False,
            "database": None,
            "collections": []
        }

    try:
        collections = db.list_collection_names()
        return {
            "connected": True,
            "database": db.name,
            "collections": collections,
            "todos_count": todos_collection.count_documents({}) if todos_collection else 0
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }
