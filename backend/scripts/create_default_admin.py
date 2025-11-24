"""
Script to create a default admin user.

This creates an admin user with predefined credentials.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timezone
import asyncio

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_default_admin():
    """Create default admin user."""
    
    print("=" * 60)
    print("CREATE DEFAULT ADMIN USER")
    print("=" * 60)
    
    # Admin credentials
    admin_email = "admin@uabc.edu.mx"
    admin_password = "12345678"
    admin_name = "Administrador"
    
    # Get MongoDB connection
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'breast_cancer_dashboard')
    
    if not mongo_url:
        print("❌ Error: MONGO_URL not set in .env file")
        return
    
    client = None
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        print(f"✅ Connected to MongoDB: {db_name}")
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": admin_email})
        if existing_user:
            print(f"⚠️  User '{admin_email}' already exists")
            print("\nExisting credentials:")
            print(f"Email: {admin_email}")
            print(f"Password: {admin_password}")
            return
        
        # Create user
        hashed_password = pwd_context.hash(admin_password)
        user_dict = {
            "email": admin_email,
            "full_name": admin_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.users.insert_one(user_dict)
        
        print("\n" + "=" * 60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📧 Email:    {admin_email}")
        print(f"🔑 Password: {admin_password}")
        print(f"👤 Name:     {admin_name}")
        print("\n⚠️  IMPORTANT: Change this password after first login!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if client is not None:
            client.close()
            print("\n✅ MongoDB connection closed")


if __name__ == "__main__":
    asyncio.run(create_default_admin())

