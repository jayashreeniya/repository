import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def test_token_access():
    """Test if the token can access any bases"""
    print("🔍 Testing Token Access...")
    
    token = os.getenv("AIRTABLE_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Get user info
    try:
        response = requests.get("https://api.airtable.com/v0/meta/whoami", headers=headers)
        print(f"Whoami Status: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Token is valid for user: {user_info.get('id', 'Unknown')}")
        else:
            print(f"❌ Token validation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False
    
    # Test 2: List accessible bases
    try:
        response = requests.get("https://api.airtable.com/v0/meta/bases", headers=headers)
        print(f"Bases Status: {response.status_code}")
        if response.status_code == 200:
            bases = response.json()
            print(f"✅ Found {len(bases.get('bases', []))} accessible bases:")
            for base in bases.get('bases', []):
                print(f"   - {base.get('name', 'Unknown')} (ID: {base.get('id', 'Unknown')})")
        else:
            print(f"❌ Cannot list bases: {response.text}")
    except Exception as e:
        print(f"❌ Error listing bases: {e}")
    
    return True

def test_specific_bases():
    """Test access to specific bases"""
    print("\n🔍 Testing Specific Bases...")
    
    token = os.getenv("AIRTABLE_TOKEN")
    leads_base_id = os.getenv("LEADS_BASE_ID")
    kpis_base_id = os.getenv("KPIS_BASE_ID")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test Leads Base
    print(f"\n📊 Testing Leads Base: {leads_base_id}")
    try:
        # First, try to get base schema
        response = requests.get(f"https://api.airtable.com/v0/meta/bases/{leads_base_id}/tables", headers=headers)
        print(f"Schema Status: {response.status_code}")
        if response.status_code == 200:
            tables = response.json()
            print(f"✅ Found {len(tables.get('tables', []))} tables in Leads base:")
            for table in tables.get('tables', []):
                print(f"   - {table.get('name', 'Unknown')} (ID: {table.get('id', 'Unknown')})")
        else:
            print(f"❌ Cannot access Leads base schema: {response.text}")
    except Exception as e:
        print(f"❌ Error accessing Leads base: {e}")
    
    # Test KPIs Base
    print(f"\n📈 Testing KPIs Base: {kpis_base_id}")
    try:
        response = requests.get(f"https://api.airtable.com/v0/meta/bases/{kpis_base_id}/tables", headers=headers)
        print(f"Schema Status: {response.status_code}")
        if response.status_code == 200:
            tables = response.json()
            print(f"✅ Found {len(tables.get('tables', []))} tables in KPIs base:")
            for table in tables.get('tables', []):
                print(f"   - {table.get('name', 'Unknown')} (ID: {table.get('id', 'Unknown')})")
        else:
            print(f"❌ Cannot access KPIs base schema: {response.text}")
    except Exception as e:
        print(f"❌ Error accessing KPIs base: {e}")

def test_table_access():
    """Test access to specific tables"""
    print("\n🔍 Testing Table Access...")
    
    token = os.getenv("AIRTABLE_TOKEN")
    leads_base_id = os.getenv("LEADS_BASE_ID")
    kpis_base_id = os.getenv("KPIS_BASE_ID")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Common table names to try
    leads_table_names = ["Leads", "leads", "Lead", "lead", "Contacts", "contacts"]
    kpis_table_names = ["Weekly KPIs", "KPIs", "kpis", "Metrics", "metrics", "Weekly", "weekly"]
    
    # Test Leads tables
    print(f"\n📊 Testing Leads tables in base: {leads_base_id}")
    for table_name in leads_table_names:
        try:
            url = f"https://api.airtable.com/v0/{leads_base_id}/{table_name}"
            response = requests.get(url, headers=headers, params={"maxRecords": 1})
            print(f"Table '{table_name}': {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Successfully accessed table: {table_name}")
                data = response.json()
                if 'records' in data:
                    print(f"   Found {len(data['records'])} records")
                break
            elif response.status_code == 404:
                print(f"   Table '{table_name}' not found")
            else:
                print(f"   Error: {response.text[:100]}")
        except Exception as e:
            print(f"   Error testing '{table_name}': {e}")
    
    # Test KPIs tables
    print(f"\n📈 Testing KPIs tables in base: {kpis_base_id}")
    for table_name in kpis_table_names:
        try:
            url = f"https://api.airtable.com/v0/{kpis_base_id}/{table_name}"
            response = requests.get(url, headers=headers, params={"maxRecords": 1})
            print(f"Table '{table_name}': {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Successfully accessed table: {table_name}")
                data = response.json()
                if 'records' in data:
                    print(f"   Found {len(data['records'])} records")
                break
            elif response.status_code == 404:
                print(f"   Table '{table_name}' not found")
            else:
                print(f"   Error: {response.text[:100]}")
        except Exception as e:
            print(f"   Error testing '{table_name}': {e}")

def main():
    """Run comprehensive Airtable diagnostics"""
    print("🔧 Airtable Connection Diagnostics")
    print("=" * 50)
    
    # Check environment variables
    token = os.getenv("AIRTABLE_TOKEN")
    leads_base_id = os.getenv("LEADS_BASE_ID")
    kpis_base_id = os.getenv("KPIS_BASE_ID")
    
    print(f"Token: {token[:20]}..." if token else "❌ No token found")
    print(f"Leads Base ID: {leads_base_id}")
    print(f"KPIs Base ID: {kpis_base_id}")
    
    if not all([token, leads_base_id, kpis_base_id]):
        print("❌ Missing required environment variables")
        return
    
    # Run diagnostics
    if test_token_access():
        test_specific_bases()
        test_table_access()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("1. If token validation failed, check your Personal Access Token")
    print("2. If bases are not accessible, ensure the token has access to these specific bases")
    print("3. If tables are not found, check the exact table names in your Airtable bases")
    print("4. Make sure the token has read/write permissions for both bases")

if __name__ == "__main__":
    main() 