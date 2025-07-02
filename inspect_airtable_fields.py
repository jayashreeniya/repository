#!/usr/bin/env python3
"""
Inspect Airtable table fields to see actual column names
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID")
KPIS_BASE_ID = os.getenv("KPIS_BASE_ID")

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

def inspect_table_fields(base_id, table_name):
    """Inspect the fields in a specific table"""
    print(f"\n🔍 Inspecting table: '{table_name}' in base {base_id}")
    
    # Get table schema
    schema_url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    response = requests.get(schema_url, headers=headers)
    
    if response.status_code == 200:
        tables = response.json().get('tables', [])
        for table in tables:
            if table['name'] == table_name:
                print(f"✅ Found table: {table['name']} (ID: {table['id']})")
                print("\n📋 Field names:")
                for field in table['fields']:
                    field_type = field.get('type', 'unknown')
                    print(f"   - {field['name']} ({field_type})")
                return table['fields']
    else:
        print(f"❌ Failed to get schema: {response.status_code}")
        return []

def inspect_sample_data(base_id, table_name):
    """Get sample data to see actual field values"""
    print(f"\n📊 Sample data from '{table_name}':")
    
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    response = requests.get(url, headers=headers, params={"maxRecords": 3})
    
    if response.status_code == 200:
        data = response.json()
        records = data.get('records', [])
        
        if records:
            print(f"✅ Found {len(records)} records")
            for i, record in enumerate(records):
                print(f"\n📝 Record {i+1}:")
                fields = record.get('fields', {})
                if fields:
                    for field_name, field_value in fields.items():
                        print(f"   {field_name}: {field_value}")
                else:
                    print("   (No fields)")
        else:
            print("   (No records found)")
    else:
        print(f"❌ Failed to get data: {response.status_code}")

def main():
    print("🔧 Airtable Field Inspection")
    print("=" * 50)
    
    # Inspect Leads table
    leads_fields = inspect_table_fields(LEADS_BASE_ID, "Imported table")
    inspect_sample_data(LEADS_BASE_ID, "Imported table")
    
    # Inspect KPIs table
    kpis_fields = inspect_table_fields(KPIS_BASE_ID, "Imported table")
    inspect_sample_data(KPIS_BASE_ID, "Imported table")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("=" * 50)
    
    if leads_fields:
        print(f"\n🎯 Leads table has {len(leads_fields)} fields:")
        for field in leads_fields:
            print(f"   - {field['name']}")
    
    if kpis_fields:
        print(f"\n📈 KPIs table has {len(kpis_fields)} fields:")
        for field in kpis_fields:
            print(f"   - {field['name']}")

if __name__ == "__main__":
    main() 