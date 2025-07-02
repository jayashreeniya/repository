import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_correct_tables():
    """Test access to the correct table names"""
    print("🔍 Testing Correct Table Names...")
    
    token = os.getenv("AIRTABLE_TOKEN")
    leads_base_id = os.getenv("LEADS_BASE_ID")
    kpis_base_id = os.getenv("KPIS_BASE_ID")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test Leads table with correct name
    print(f"\n📊 Testing Leads table: 'Imported table' in base {leads_base_id}")
    try:
        # URL encode the table name since it has spaces
        import urllib.parse
        table_name_encoded = urllib.parse.quote("Imported table")
        url = f"https://api.airtable.com/v0/{leads_base_id}/{table_name_encoded}"
        response = requests.get(url, headers=headers, params={"maxRecords": 5})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully accessed Leads table!")
            print(f"   Found {len(data.get('records', []))} records")
            
            # Show first record structure
            if data.get('records'):
                first_record = data['records'][0]
                print(f"   First record fields: {list(first_record.get('fields', {}).keys())}")
                print(f"   Sample data: {first_record.get('fields', {})}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test KPIs table with correct name
    print(f"\n📈 Testing KPIs table: 'Imported table' in base {kpis_base_id}")
    try:
        table_name_encoded = urllib.parse.quote("Imported table")
        url = f"https://api.airtable.com/v0/{kpis_base_id}/{table_name_encoded}"
        response = requests.get(url, headers=headers, params={"maxRecords": 5})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully accessed KPIs table!")
            print(f"   Found {len(data.get('records', []))} records")
            
            # Show first record structure
            if data.get('records'):
                first_record = data['records'][0]
                print(f"   First record fields: {list(first_record.get('fields', {}).keys())}")
                print(f"   Sample data: {first_record.get('fields', {})}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_correct_tables() 