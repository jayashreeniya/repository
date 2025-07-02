#!/usr/bin/env python3
"""
Add test leads to Airtable for Niya agent testing
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID")

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

def add_test_leads():
    """Add sample test leads to Airtable"""
    
    test_leads = [
        {
            "Lead Name": "Sarah Johnson",
            "Company Name": "TechFlow Solutions",
            "Website/LinkedIn": "https://linkedin.com/in/sarahjohnson",
            "Industry": "SaaS",
            "Company Size": "201-500 employees",
            "Role": "VP of Engineering",
            "Email": "sarah.johnson@techflow.com",
            "Email Sent?": "FALSE",
            "Status": "New Lead"
        },
        {
            "Lead Name": "Michael Chen",
            "Company Name": "DataSync Inc",
            "Website/LinkedIn": "https://linkedin.com/in/michaelchen",
            "Industry": "Technology",
            "Company Size": "51-200 employees",
            "Role": "CTO",
            "Email": "mchen@datasync.com",
            "Email Sent?": "FALSE",
            "Status": "New Lead"
        },
        {
            "Lead Name": "Emily Rodriguez",
            "Company Name": "CloudScale Systems",
            "Website/LinkedIn": "https://linkedin.com/in/emilyrodriguez",
            "Industry": "Cloud Computing",
            "Company Size": "500-1000 employees",
            "Role": "Director of Operations",
            "Email": "emily.rodriguez@cloudscale.com",
            "Email Sent?": "FALSE",
            "Status": "New Lead"
        }
    ]
    
    url = f"https://api.airtable.com/v0/{LEADS_BASE_ID}/Imported table"
    
    print("🚀 Adding test leads to Airtable...")
    
    for i, lead in enumerate(test_leads):
        payload = {
            "records": [{
                "fields": lead
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Added lead {i+1}: {lead['Lead Name']} at {lead['Company Name']}")
        else:
            print(f"❌ Failed to add lead {i+1}: {response.status_code} - {response.text}")
    
    print(f"\n🎯 Added {len(test_leads)} test leads successfully!")

def check_existing_leads():
    """Check existing leads in the table"""
    url = f"https://api.airtable.com/v0/{LEADS_BASE_ID}/Imported table"
    response = requests.get(url, headers=headers, params={"maxRecords": 10})
    
    if response.status_code == 200:
        data = response.json()
        records = data.get('records', [])
        print(f"\n📊 Current leads in table: {len(records)}")
        
        for record in records:
            fields = record.get('fields', {})
            name = fields.get('Lead Name', 'Unknown')
            company = fields.get('Company Name', 'Unknown')
            email_sent = fields.get('Email Sent?', 'Unknown')
            print(f"   - {name} at {company} (Email Sent: {email_sent})")
    else:
        print(f"❌ Failed to check leads: {response.status_code}")

if __name__ == "__main__":
    print("🔧 Test Lead Management")
    print("=" * 40)
    
    # Check existing leads first
    check_existing_leads()
    
    # Add test leads
    add_test_leads()
    
    # Check again
    check_existing_leads() 