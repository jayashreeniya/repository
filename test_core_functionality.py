import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def test_openai_email_generation():
    """Test OpenAI email generation"""
    print("🧪 Testing OpenAI Email Generation...")
    
    try:
        openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test email generation
        prompt = """
        Write a compelling 3-4 line personalized outbound email from Niya to John Doe 
        who is a VP of Engineering at TechCorp.
        
        Company context: B2B SaaS company specializing in workflow automation
        Stage: Series B
        
        The email should:
        1. Be personalized and relevant to their role/company
        2. Mention their company stage if relevant
        3. Offer a 15-minute discovery call
        4. Include a Calendly link: https://calendly.com/niya/15min
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
        print("✅ Email generated successfully!")
        print("\n📧 Generated Email:")
        print("=" * 50)
        print(email_content)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Email generation failed: {e}")
        return False

def test_openai_reply_classification():
    """Test OpenAI reply classification"""
    print("\n🧪 Testing OpenAI Reply Classification...")
    
    try:
        openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test reply classification
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
        print("✅ Reply classification successful!")
        print("\n📊 Classification Result:")
        print("=" * 50)
        print(classification)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Reply classification failed: {e}")
        return False

def test_openai_demo_brief():
    """Test OpenAI demo brief generation"""
    print("\n🧪 Testing OpenAI Demo Brief Generation...")
    
    try:
        openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test demo brief generation
        lead_data = {
            "Lead Name": "Sarah Johnson",
            "Role": "VP of People",
            "Company Name": "GrowthTech",
            "Industry": "Technology",
            "Company Size": "201-1000 employees",
            "Website/LinkedIn": "https://linkedin.com/in/sarahjohnson",
            "Notes/Objections": "Interested in team wellness programs",
            "Reply Type": "Interested"
        }
        
        prompt = f"""
        Generate a 200-word demo briefing for Jayashree at Niya to pitch to the following B2B lead:

        - Lead Name: {lead_data['Lead Name']}
        - Role: {lead_data['Role']}
        - Company: {lead_data['Company Name']}
        - Industry: {lead_data['Industry']}
        - Company Size: {lead_data['Company Size']}
        - Website/LinkedIn: {lead_data['Website/LinkedIn']}
        - Notes/Objections: {lead_data['Notes/Objections']}
        - Reply Type: {lead_data['Reply Type']}

        The output should include:
        1. Summary of what the company likely does
        2. What the role's top concern might be
        3. A custom angle to pitch Niya's mental fitness bootcamp

        Keep it sharp and to the point.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        
        brief = response.choices[0].message.content.strip()
        print("✅ Demo brief generation successful!")
        print("\n📋 Generated Demo Brief:")
        print("=" * 50)
        print(brief)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo brief generation failed: {e}")
        return False

def main():
    """Run all core functionality tests"""
    print("🚀 Niya Sales Agent - Core Functionality Test")
    print("=" * 60)
    
    tests = [
        test_openai_email_generation,
        test_openai_reply_classification,
        test_openai_demo_brief
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core functionality tests passed!")
        print("   The AI components are working perfectly.")
        print("   Once Airtable permissions are fixed, the full system will work.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 