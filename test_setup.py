#!/usr/bin/env python3
"""
Test script to verify Niya Sales Agent setup
Run this script to check if all dependencies and configurations are working
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("🔍 Testing environment variables...")
    
    load_dotenv()
    
    required_vars = [
        "AIRTABLE_API_KEY",
        "AIRTABLE_BASE_ID", 
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please check your .env file")
        return False
    else:
        print("✅ All required environment variables found")
        return True

def test_dependencies():
    """Test Python dependencies"""
    print("\n🔍 Testing Python dependencies...")
    
    dependencies = [
        "openai",
        "googleapiclient",
        "google.auth",
        "airtable",
        "dotenv"
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep}")
        except ImportError:
            missing_deps.append(dep)
            print(f"❌ {dep}")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed")
        return True

def test_gmail_service():
    """Test Gmail service account file"""
    print("\n🔍 Testing Gmail service account...")
    
    if not os.path.exists("gmail-service.json"):
        print("❌ gmail-service.json not found")
        print("   Please download your Gmail service account JSON file")
        return False
    else:
        print("✅ gmail-service.json found")
        return True

def test_airtable_connection():
    """Test Airtable connection"""
    print("\n🔍 Testing Airtable connection...")
    
    try:
        from airtable import Airtable
        from dotenv import load_dotenv
        
        load_dotenv()
        
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        
        if not api_key or not base_id:
            print("❌ Airtable credentials not found in environment")
            return False
        
        # Try to connect to Airtable
        at = Airtable(base_id, "Leads", api_key)
        records = at.get_all(max_records=1)
        print("✅ Airtable connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Airtable connection failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI connection"""
    print("\n🔍 Testing OpenAI connection...")
    
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ OpenAI API key not found in environment")
            return False
        
        # Try to connect to OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI connection successful")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Niya Sales Agent - Setup Test")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_dependencies,
        test_gmail_service,
        test_airtable_connection,
        test_openai_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("   Run: python niya_agent.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 