"""
Verify Railway configuration and API connectivity.

This script checks:
1. Environment variables are set
2. OpenAI/OpenRouter API key is valid
3. Backend endpoints are accessible
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_vars():
    """Check if required environment variables are set."""
    print("🔍 Checking environment variables...")
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI/OpenRouter API key',
        'MONGO_URL': 'MongoDB connection string',
        'DB_NAME': 'Database name',
        'CORS_ORIGINS': 'CORS allowed origins'
    }
    
    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value == 'tu_nueva_api_key_aqui':
            print(f"  ❌ {var} ({description}): NOT SET")
            missing.append(var)
        else:
            # Mask sensitive values
            if 'KEY' in var or 'SECRET' in var:
                masked = value[:10] + '...' + value[-4:] if len(value) > 14 else '***'
                print(f"  ✅ {var}: {masked}")
            else:
                print(f"  ✅ {var}: {value}")
    
    return len(missing) == 0, missing

def verify_openai_key():
    """Verify OpenAI/OpenRouter API key is valid."""
    print("\n🔑 Verifying OpenAI/OpenRouter API key...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'tu_nueva_api_key_aqui':
        print("  ❌ API key not configured")
        return False
    
    # Determine if it's OpenRouter or OpenAI
    is_openrouter = api_key.startswith('sk-or-v1-')
    
    if is_openrouter:
        print("  📡 Detected OpenRouter API key")
        url = "https://openrouter.ai/api/v1/models"
    else:
        print("  📡 Detected OpenAI API key")
        url = "https://api.openai.com/v1/models"
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"  ✅ API key is valid!")
            models = response.json().get('data', [])
            print(f"  📊 Available models: {len(models)}")
            return True
        else:
            print(f"  ❌ API key validation failed: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    
    except Exception as e:
        print(f"  ❌ Error verifying API key: {str(e)}")
        return False

def verify_backend_endpoint(url):
    """Verify backend endpoint is accessible."""
    print(f"\n🌐 Checking backend endpoint: {url}")
    
    try:
        # Check root endpoint
        response = requests.get(f"{url}/api/", timeout=10)
        if response.status_code == 200:
            print(f"  ✅ Backend is accessible")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"  ❌ Backend returned status: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"  ❌ Error connecting to backend: {str(e)}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("🔧 Railway Configuration Verification")
    print("=" * 60)
    
    # Check environment variables
    env_ok, missing = check_env_vars()
    
    # Verify API key
    api_ok = verify_openai_key()
    
    # Ask for backend URL
    print("\n" + "=" * 60)
    backend_url = input("Enter your Railway backend URL (or press Enter to skip): ").strip()
    
    backend_ok = True
    if backend_url:
        backend_ok = verify_backend_endpoint(backend_url)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if env_ok and api_ok and backend_ok:
        print("✅ All checks passed! Your configuration is ready.")
        print("\n🚀 Next steps:")
        print("  1. Commit and push your changes to GitHub")
        print("  2. Railway will auto-deploy")
        print("  3. Test the AI insights in your Vercel app")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n🔧 To fix:")
        if not env_ok:
            print(f"  - Set missing environment variables: {', '.join(missing)}")
        if not api_ok:
            print("  - Get a valid API key from OpenRouter or OpenAI")
            print("    OpenRouter: https://openrouter.ai/keys")
            print("    OpenAI: https://platform.openai.com/api-keys")
        if not backend_ok:
            print("  - Check your Railway deployment logs")
            print("  - Verify the backend URL is correct")
        return 1

if __name__ == "__main__":
    sys.exit(main())

