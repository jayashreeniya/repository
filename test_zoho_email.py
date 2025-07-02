import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_zoho_email():
    """Test sending email via Zoho SMTP"""
    print("🧪 Testing Zoho Email Sending...")
    
    # Get SMTP settings from environment
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"SMTP Username: {smtp_username}")
    print(f"SMTP Password: {'*' * len(smtp_password) if smtp_password else 'Not set'}")
    
    if not all([smtp_server, smtp_username, smtp_password]):
        print("❌ Missing SMTP configuration")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = smtp_username  # Send to yourself for testing
        msg["Subject"] = "🧪 Niya Sales Agent - Zoho Email Test"
        
        # Email body
        body = """
Hello from Niya Sales Agent! 🚀

This is a test email sent via Zoho SMTP to verify that the email functionality is working correctly.

If you receive this email, it means:
✅ Zoho SMTP connection is working
✅ Authentication is successful
✅ Email sending is functional

The Niya Sales Agent is now ready to send personalized cold emails to your leads!

Best regards,
Niya Sales Agent 🤖
        """
        
        msg.attach(MIMEText(body, "plain"))
        
        # Send email
        print(f"\n📧 Sending test email to {smtp_username}...")
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            print("✅ Connected to SMTP server")
            server.login(smtp_username, smtp_password)
            print("✅ Authentication successful")
            server.sendmail(smtp_username, smtp_username, msg.as_string())
            print("✅ Email sent successfully!")
        
        print(f"\n🎉 Test email sent! Check your inbox at {smtp_username}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Please check your SMTP username and password")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_niya_email_generation():
    """Test email generation with Zoho sending"""
    print("\n🧪 Testing Niya Email Generation + Zoho Sending...")
    
    try:
        from openai import OpenAI
        
        # Generate a test email
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
        
        # Split into subject and body
        lines = email_content.split('\n')
        subject = lines[0].replace('Subject:', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        print(f"📧 Generated Email:")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        
        # Send the generated email
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", "465"))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = smtp_username  # Send to yourself for testing
        msg["Subject"] = f"🧪 {subject}"
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, smtp_username, msg.as_string())
        
        print("✅ Generated email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in email generation test: {e}")
        return False

def main():
    """Run all Zoho email tests"""
    print("🚀 Niya Sales Agent - Zoho Email Test")
    print("=" * 50)
    
    tests = [
        test_zoho_email,
        test_niya_email_generation
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
        print("🎉 All Zoho email tests passed!")
        print("   Your email system is ready for production use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 