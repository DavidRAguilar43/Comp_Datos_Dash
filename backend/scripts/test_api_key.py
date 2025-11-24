"""
Test script to verify OpenAI/OpenRouter API key.

This script tests if the API key in .env is valid.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

def test_api_key():
    """Test if the API key works."""
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        return False
    
    print(f"✅ API key found: {api_key[:15]}...")
    print(f"   Length: {len(api_key)} characters")
    
    # Check if it's OpenRouter or OpenAI
    if api_key.startswith('sk-or-v1-'):
        print("🔄 Detected OpenRouter API key")
        base_url = "https://openrouter.ai/api/v1"
    elif api_key.startswith('sk-proj-'):
        print("🔄 Detected OpenAI API key")
        base_url = None
    else:
        print("⚠️  WARNING: API key format not recognized")
        base_url = None
    
    # Try to make a simple API call
    try:
        print("\n🧪 Testing API call...")
        
        if base_url:
            client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using cheaper model for testing
            messages=[
                {"role": "user", "content": "Say 'API key works!' if you can read this."}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        print(f"✅ SUCCESS! API response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: API call failed")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        
        if "401" in str(e):
            print("\n💡 SOLUTION:")
            print("   Your API key is invalid or expired.")
            print("   Please get a new API key from:")
            if base_url:
                print("   https://openrouter.ai/keys")
            else:
                print("   https://platform.openai.com/api-keys")
        
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔑 OpenAI/OpenRouter API Key Test")
    print("=" * 60)
    
    success = test_api_key()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ API key is valid and working!")
    else:
        print("❌ API key test failed. Please update your .env file.")
    print("=" * 60)

