import os
from dotenv import load_dotenv

load_dotenv()

def test_system_without_email():
    """Test the full system without email sending"""
    print("🧪 Testing Full System (Without Email Sending)")
    print("=" * 50)
    
    # Test 1: Airtable connection
    print("\n📊 Testing Airtable Connection...")
    try:
        import requests
        token = os.getenv("AIRTABLE_TOKEN")
        leads_base_id = os.getenv("LEADS_BASE_ID")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        import urllib.parse
        table_name_encoded = urllib.parse.quote("Imported table")
        url = f"https://api.airtable.com/v0/{leads_base_id}/{table_name_encoded}"
        response = requests.get(url, headers=headers, params={"maxRecords": 1})
        
        if response.status_code == 200:
            print("✅ Airtable connection successful")
        else:
            print(f"❌ Airtable connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Airtable test failed: {e}")
        return False
    
    # Test 2: OpenAI email generation
    print("\n🤖 Testing OpenAI Email Generation...")
    try:
        from openai import OpenAI
        openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = """
        Write a compelling 3-4 line personalized outbound email from Niya to John Doe 
        who is a VP of Engineering at TechCorp.
        
        Company context: B2B SaaS company specializing in workflow automation
        Stage: Series B
        
        The email should:
        1. Be personalized and relevant to their role/company
        2. Mention their company stage if relevant
        3. Offer a 15-minute discovery call
        4. Include a Calendly link: https://calendly.com/niya-nidhil/introductory-call
        5. Be professional but conversational
        6. End with a clear call-to-action
        
        Format: Subject line on first line, then email body.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        
        email_content = response.choices[0].message.content.strip()
        print("✅ Email generation successful")
        print(f"📧 Generated email preview: {email_content[:100]}...")
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False
    
    # Test 3: Reply classification
    print("\n📊 Testing Reply Classification...")
    try:
        reply_text = "Thanks for reaching out! I'm interested in learning more about your mental fitness bootcamp. Can we schedule a call next week?"
        
        prompt = f"""
        Analyze this email reply and classify it into one of these categories:
        - Interested: Wants to learn more, asks questions, shows genuine interest
        - Later: Not ready now but might be interested later, asks to follow up
        - Not Now: Not interested, objections, declines
        - Wrong Person: Not the right contact, should be someone else
        - Meeting Booked: Confirms meeting or calendar booking via Calendly
        
        Reply: {reply_text}
        
        Return JSON format:
        {{
            "category": "Interested/Later/Not Now/Wrong Person/Meeting Booked",
            "confidence": 0.95,
            "key_points": ["point1", "point2"],
            "next_action": "suggested next step",
            "calendly_clicked": true/false
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )
        
        classification = response.choices[0].message.content.strip()
        print("✅ Reply classification successful")
        print(f"📊 Classification: {classification[:100]}...")
        
    except Exception as e:
        print(f"❌ Reply classification test failed: {e}")
        return False
    
    return True

def main():
    """Run system tests without email"""
    print("🚀 Niya Sales Agent - System Test (No Email)")
    print("=" * 60)
    
    if test_system_without_email():
        print("\n🎉 All core system tests passed!")
        print("✅ Airtable connection working")
        print("✅ OpenAI email generation working")
        print("✅ Reply classification working")
        print("\n💡 The system is ready to use!")
        print("   Email sending can be configured later.")
        print("   You can run: python niya_agent.py")
    else:
        print("\n❌ Some system tests failed")
        print("   Please check the errors above")

if __name__ == "__main__":
    main() 