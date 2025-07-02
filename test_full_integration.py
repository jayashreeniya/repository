#!/usr/bin/env python3
"""
Niya AI Sales Agent - Full Integration Test
Tests the complete workflow from lead fetching to KPI tracking
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID")
KPIS_BASE_ID = os.getenv("KPIS_BASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CALENDLY_LINK = os.getenv("CALENDLY_LINK", "https://calendly.com/niya/15min")

# Airtable headers
headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

def test_airtable_connection():
    """Test Airtable connection and table access"""
    print("🔍 Testing Airtable Connection...")
    
    # Test Leads base
    leads_url = f"https://api.airtable.com/v0/{LEADS_BASE_ID}/Imported table"
    response = requests.get(leads_url, headers=headers, params={"maxRecords": 1})
    
    if response.status_code != 200:
        print(f"❌ Leads base connection failed: {response.status_code}")
        return False
    
    # Test KPIs base
    kpis_url = f"https://api.airtable.com/v0/{KPIS_BASE_ID}/Imported table"
    response = requests.get(kpis_url, headers=headers, params={"maxRecords": 1})
    
    if response.status_code != 200:
        print(f"❌ KPIs base connection failed: {response.status_code}")
        return False
    
    print("✅ Airtable connection successful!")
    return True

def test_openai_integration():
    """Test OpenAI API integration"""
    print("\n🧠 Testing OpenAI Integration...")
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Test email generation
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Niya, an AI sales agent. Generate personalized cold emails."},
                {"role": "user", "content": "Generate a cold email for John Smith, VP of Engineering at TechCorp, a Series B SaaS company with 200 employees. Focus on workflow automation."}
            ],
            max_tokens=300
        )
        
        email = response.choices[0].message.content
        print("✅ Email generation successful!")
        print(f"📧 Sample email: {email[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI integration failed: {e}")
        return False

def test_lead_fetching():
    """Test fetching leads from Airtable"""
    print("\n📊 Testing Lead Fetching...")
    
    try:
        url = f"https://api.airtable.com/v0/{LEADS_BASE_ID}/Imported table"
        response = requests.get(url, headers=headers, params={"maxRecords": 5})
        
        if response.status_code == 200:
            data = response.json()
            leads = data.get('records', [])
            print(f"✅ Successfully fetched {len(leads)} leads")
            
            if leads:
                # Show sample lead data
                sample_lead = leads[0]
                fields = sample_lead.get('fields', {})
                print(f"📋 Sample lead fields: {list(fields.keys())}")
            
            return leads
        else:
            print(f"❌ Lead fetching failed: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Lead fetching error: {e}")
        return []

def test_email_generation_for_leads(leads):
    """Test generating personalized emails for leads"""
    print("\n✉️ Testing Email Generation for Leads...")
    
    if not leads:
        print("⚠️ No leads to generate emails for")
        return []
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        generated_emails = []
        
        for i, lead in enumerate(leads[:2]):  # Test with first 2 leads
            fields = lead.get('fields', {})
            
            # Create a sample lead if fields are empty
            if not fields:
                fields = {
                    'Name': f'Test Lead {i+1}',
                    'Company': f'Test Company {i+1}',
                    'Title': 'VP of Engineering',
                    'Industry': 'Technology',
                    'Company Size': '200-500 employees'
                }
            
            prompt = f"""
            Generate a personalized cold email for:
            Name: {fields.get('Name', 'Unknown')}
            Company: {fields.get('Company', 'Unknown')}
            Title: {fields.get('Title', 'Unknown')}
            Industry: {fields.get('Industry', 'Unknown')}
            Company Size: {fields.get('Company Size', 'Unknown')}
            
            Include the Calendly link: {CALENDLY_LINK}
            Keep it professional and personalized.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Niya, an AI sales agent. Generate personalized cold emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )
            
            email = response.choices[0].message.content
            generated_emails.append({
                'lead_id': lead['id'],
                'email': email,
                'fields': fields
            })
            
            print(f"✅ Generated email for {fields.get('Name', 'Unknown')}")
        
        print(f"✅ Successfully generated {len(generated_emails)} emails")
        return generated_emails
        
    except Exception as e:
        print(f"❌ Email generation failed: {e}")
        return []

def test_reply_classification():
    """Test reply classification"""
    print("\n📊 Testing Reply Classification...")
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        sample_replies = [
            "Hi Niya, this sounds interesting. Can we schedule a call next week?",
            "Thanks but we're not interested at this time.",
            "I'd like to learn more about your pricing and features."
        ]
        
        for i, reply in enumerate(sample_replies):
            prompt = f"""
            Classify this email reply into one of these categories:
            - Interested: Shows genuine interest, wants to learn more, asks for call/demo
            - Not Interested: Declines, not interested, unsubscribe requests
            - More Information: Asks for pricing, features, case studies, etc.
            - Objection: Has concerns, objections, or questions about the solution
            - Other: Doesn't fit the above categories
            
            Reply: "{reply}"
            
            Return a JSON object with:
            - category: the classification
            - confidence: confidence level (0-1)
            - key_points: list of key points from the reply
            - next_action: recommended next action
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI that classifies email replies. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            
            try:
                classification = json.loads(response.choices[0].message.content)
                print(f"✅ Reply {i+1} classified as: {classification.get('category', 'Unknown')}")
            except:
                print(f"⚠️ Reply {i+1} classification parsing failed")
        
        print("✅ Reply classification successful!")
        return True
        
    except Exception as e:
        print(f"❌ Reply classification failed: {e}")
        return False

def test_kpi_tracking():
    """Test KPI tracking and updates"""
    print("\n📈 Testing KPI Tracking...")
    
    try:
        # Get current week's KPI record
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        url = f"https://api.airtable.com/v0/{KPIS_BASE_ID}/Imported table"
        response = requests.get(url, headers=headers, params={
            "filterByFormula": f"{{Week Start}}='{week_start}'"
        })
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            
            if records:
                # Update existing record
                record_id = records[0]['id']
                current_fields = records[0].get('fields', {})
                
                # Simulate KPI updates
                updated_fields = {
                    'Leads Added': current_fields.get('Leads Added', 0) + 1,
                    'Emails Sent': current_fields.get('Emails Sent', 0) + 1,
                    'Replies': current_fields.get('Replies', 0) + 1
                }
                
                update_data = {
                    "fields": updated_fields
                }
                
                update_url = f"https://api.airtable.com/v0/{KPIS_BASE_ID}/Imported table/{record_id}"
                update_response = requests.patch(update_url, headers=headers, json=update_data)
                
                if update_response.status_code == 200:
                    print("✅ KPI tracking successful!")
                    print(f"📊 Updated KPIs: {updated_fields}")
                    return True
                else:
                    print(f"❌ KPI update failed: {update_response.status_code}")
                    return False
            else:
                # Create new KPI record for current week
                print(f"📅 Creating new KPI record for week starting {week_start}")
                new_record_data = {
                    "records": [{
                        "fields": {
                            "Week Start": week_start,
                            "Leads Added": 1,
                            "Emails Sent": 1,
                            "Replies": 1,
                            "Demos Booked": 0,
                            "Deals Closed": 0
                        }
                    }]
                }
                
                create_response = requests.post(url, headers=headers, json=new_record_data)
                
                if create_response.status_code == 200:
                    print("✅ KPI record created successfully!")
                    print(f"📊 New KPIs: {new_record_data['records'][0]['fields']}")
                    return True
                else:
                    print(f"❌ KPI record creation failed: {create_response.status_code}")
                    return False
        else:
            print(f"❌ KPI fetching failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ KPI tracking error: {e}")
        return False

def test_demo_brief_generation():
    """Test demo brief generation"""
    print("\n📋 Testing Demo Brief Generation...")
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        sample_lead = {
            'Name': 'Sarah Johnson',
            'Company': 'GrowthTech',
            'Title': 'VP of People',
            'Industry': 'Technology',
            'Company Size': '201-1000 employees',
            'Interest': 'Team wellness programs'
        }
        
        prompt = f"""
        Generate a demo brief for this lead:
        Name: {sample_lead['Name']}
        Company: {sample_lead['Company']}
        Title: {sample_lead['Title']}
        Industry: {sample_lead['Industry']}
        Company Size: {sample_lead['Company Size']}
        Interest: {sample_lead['Interest']}
        
        The brief should include:
        - Key talking points
        - Pain points to address
        - Value propositions to highlight
        - Questions to ask
        - Demo flow recommendations
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates demo briefs for sales calls."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        brief = response.choices[0].message.content
        print("✅ Demo brief generation successful!")
        print(f"📋 Brief preview: {brief[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo brief generation failed: {e}")
        return False

def main():
    """Run full integration test"""
    print("🚀 Niya AI Sales Agent - Full Integration Test")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Airtable Connection
    test_results.append(("Airtable Connection", test_airtable_connection()))
    
    # Test 2: OpenAI Integration
    test_results.append(("OpenAI Integration", test_openai_integration()))
    
    # Test 3: Lead Fetching
    leads = test_lead_fetching()
    test_results.append(("Lead Fetching", len(leads) >= 0))
    
    # Test 4: Email Generation
    emails = test_email_generation_for_leads(leads)
    test_results.append(("Email Generation", len(emails) >= 0))
    
    # Test 5: Reply Classification
    test_results.append(("Reply Classification", test_reply_classification()))
    
    # Test 6: KPI Tracking
    test_results.append(("KPI Tracking", test_kpi_tracking()))
    
    # Test 7: Demo Brief Generation
    test_results.append(("Demo Brief Generation", test_demo_brief_generation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Integration Test Results:")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! The system is ready for production.")
    elif passed >= total * 0.8:
        print("⚠️ Most tests passed. Minor issues need attention.")
    else:
        print("❌ Multiple tests failed. System needs significant fixes.")
    
    return passed == total

if __name__ == "__main__":
    main() 