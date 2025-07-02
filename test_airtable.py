import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials from .env
token = os.getenv("AIRTABLE_TOKEN")
leads_base_id = os.getenv("LEADS_BASE_ID")
kpis_base_id = os.getenv("KPIS_BASE_ID")

print(f"Token: {token[:20]}..." if token else "No token found")
print(f"Leads Base ID: {leads_base_id}")
print(f"KPIs Base ID: {kpis_base_id}")

# Test Leads base
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("\n🔍 Testing Leads Base...")
try:
    url = f"https://api.airtable.com/v0/{leads_base_id}/Imported table"
    response = requests.get(url, headers=headers, params={"maxRecords": 1})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        print("✅ Leads base connection successful!")
    else:
        print(f"❌ Leads base connection failed: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🔍 Testing KPIs Base...")
try:
    url = f"https://api.airtable.com/v0/{kpis_base_id}/Imported table"
    response = requests.get(url, headers=headers, params={"maxRecords": 1})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        print("✅ KPIs base connection successful!")
    else:
        print(f"❌ KPIs base connection failed: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}") 