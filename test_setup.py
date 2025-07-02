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
        "AIRTABLE_TOKEN",
        "LEADS_BASE_ID", 
        "KPIS_BASE_ID",
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
        "requests",
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

def test_email_configuration():
    """Test email configuration (Gmail or SMTP)"""
    print("\n🔍 Testing email configuration...")
    
    email_provider = os.getenv("EMAIL_PROVIDER", "gmail").lower()
    
    if email_provider == "gmail":
        if not os.path.exists("gmail-service.json"):
            print("❌ gmail-service.json not found")
            print("   Please download your Gmail service account JSON file")
            return False
        else:
            print("✅ gmail-service.json found")
            return True
    else:
        # Test SMTP configuration
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not all([smtp_server, smtp_username, smtp_password]):
            print("❌ SMTP configuration incomplete")
            print("   Please check SMTP_SERVER, SMTP_USERNAME, and SMTP_PASSWORD in .env")
            return False
        
        print(f"✅ SMTP configuration found: {smtp_server}")
        return True

def test_airtable_connection():
    """Test Airtable connections"""
    print("\n🔍 Testing Airtable connections...")
    
    try:
        import requests
        from dotenv import load_dotenv
        
        load_dotenv()
        
        token = os.getenv("AIRTABLE_TOKEN")
        leads_base_id = os.getenv("LEADS_BASE_ID")
        kpis_base_id = os.getenv("KPIS_BASE_ID")
        
        if not token or not leads_base_id or not kpis_base_id:
            print("❌ Airtable credentials not found in environment")
            return False
        
        # Try to connect to both Airtable bases
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test Leads base
        import urllib.parse
        leads_table_encoded = urllib.parse.quote("Imported table")
        leads_url = f"https://api.airtable.com/v0/{leads_base_id}/{leads_table_encoded}"
        leads_response = requests.get(leads_url, headers=headers, params={"maxRecords": 1})
        leads_response.raise_for_status()
        print("✅ Leads base connection successful")
        
        # Test KPIs base
        kpis_table_encoded = urllib.parse.quote("Imported table")
        kpis_url = f"https://api.airtable.com/v0/{kpis_base_id}/{kpis_table_encoded}"
        kpis_response = requests.get(kpis_url, headers=headers, params={"maxRecords": 1})
        kpis_response.raise_for_status()
        print("✅ KPIs base connection successful")
        
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
        test_email_configuration,
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