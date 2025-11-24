"""
Script to create an admin user directly in the database.

Usage:
    python scripts/create_admin_user.py

This script will prompt for email, password, and full name,
then create the user in the MongoDB database.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from services.auth import AuthService
from datetime import datetime, timezone
import asyncio

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')


async def create_admin_user():
    """
    Create an admin user in the database.
    
    Prompts for user information and creates the user with hashed password.
    """
    print("=" * 60)
    print("CREATE ADMIN USER")
    print("=" * 60)
    
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

        # Initialize auth service
        auth_service = AuthService(db)
        
        # Get user information
        print("\nEnter user information:")
        email = input("Email: ").strip()
        
        # Check if user already exists
        existing_user = await auth_service.get_user(email)
        if existing_user:
            print(f"❌ Error: User with email '{email}' already exists")
            client.close()
            return
        
        full_name = input("Full Name: ").strip()
        password = input("Password (min 8 characters): ").strip()
        
        # Validate password
        if len(password) < 8:
            print("❌ Error: Password must be at least 8 characters")
            client.close()
            return
        
        # Create user
        hashed_password = auth_service.get_password_hash(password)
        user_dict = {
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.users.insert_one(user_dict)
        
        print("\n" + "=" * 60)
        print("✅ Admin user created successfully!")
        print("=" * 60)
        print(f"Email: {email}")
        print(f"Name: {full_name}")
        print("\nYou can now login with these credentials.")
        print("=" * 60)
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'client' in locals():
            client.close()


if __name__ == "__main__":
    asyncio.run(create_admin_user())

