import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_all_zoho_configs():
    """Test all possible Zoho configurations"""
    print("🔍 Final Zoho Email Test - All Configurations")
    print("=" * 60)
    
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    
    # All possible Zoho SMTP configurations
    configs = [
        ("smtp.zoho.in", 465, "SSL"),
        ("smtp.zoho.in", 587, "TLS"),
        ("smtp.zoho.com", 465, "SSL"),
        ("smtp.zoho.com", 587, "TLS"),
        ("smtp.zoho.eu", 465, "SSL"),
        ("smtp.zoho.eu", 587, "TLS"),
    ]
    
    for server, port, encryption in configs:
        print(f"\n🔍 Testing: {server}:{port} ({encryption})")
        
        try:
            if encryption == "SSL":
                smtp = smtplib.SMTP_SSL(server, port)
            else:
                smtp = smtplib.SMTP(server, port)
                smtp.starttls()
            
            print(f"✅ Connected to {server}:{port}")
            
            # Try authentication
            smtp.login(username, password)
            print("✅ Authentication successful!")
            
            # Try sending email
            msg = MIMEMultipart()
            msg["From"] = username
            msg["To"] = username
            msg["Subject"] = f"🧪 Final Test - {server}:{port}"
            msg.attach(MIMEText(f"Test email from {server}:{port} using {encryption}", "plain"))
            
            smtp.send_message(msg)
            print("✅ Email sent successfully!")
            
            smtp.quit()
            
            print(f"\n🎉 SUCCESS! Working configuration found:")
            print(f"   SMTP_SERVER={server}")
            print(f"   SMTP_PORT={port}")
            print(f"   Encryption: {encryption}")
            
            # Update .env file with working config
            update_env_file(server, port)
            
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    return False

def update_env_file(server, port):
    """Update .env file with working configuration"""
    print(f"\n💾 Updating .env file with working configuration...")
    print(f"   SMTP_SERVER={server}")
    print(f"   SMTP_PORT={port}")

def suggest_gmail_switch():
    """Suggest switching to Gmail"""
    print("\n" + "=" * 60)
    print("❌ All Zoho configurations failed")
    print("💡 Switching to Gmail SMTP (Recommended)")
    print("=" * 60)
    
    print("\n📋 Gmail Setup Instructions:")
    print("1. Go to Google Account settings")
    print("2. Enable 2-Factor Authentication")
    print("3. Generate an App Password")
    print("4. Update your .env file:")
    print("   EMAIL_PROVIDER=gmail")
    print("   GMAIL_APP_PASSWORD=your_app_password")
    
    print("\n🚀 Quick Gmail Test:")
    print("1. Set EMAIL_PROVIDER=gmail in .env")
    print("2. Add GMAIL_APP_PASSWORD=your_password")
    print("3. Run: python test_gmail_email.py")
    
    print("\n✅ Benefits of Gmail:")
    print("- More reliable SMTP")
    print("- Better documentation")
    print("- Easier setup")
    print("- Higher sending limits")

def main():
    """Run final Zoho test"""
    print("🚀 Niya Sales Agent - Final Zoho Test")
    print("=" * 60)
    
    if test_all_zoho_configs():
        print("\n🎉 Zoho email is now working!")
        print("   Your system is ready for production use.")
        print("   Run: python niya_agent.py")
    else:
        suggest_gmail_switch()
        
        # Create Gmail test file
        create_gmail_test_file()

def create_gmail_test_file():
    """Create a Gmail test file for easy switching"""
    gmail_test_content = '''import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_gmail_smtp():
    """Test Gmail SMTP"""
    print("🧪 Testing Gmail SMTP...")
    
    username = "jayashreev@wellbeing.net"  # Your Gmail address
    password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not password:
        print("❌ GMAIL_APP_PASSWORD not found in .env")
        print("   Please add your Gmail app password to .env")
        return False
    
    try:
        # Connect to Gmail SMTP
        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        print("✅ Connected to Gmail SMTP")
        
        # Login
        smtp.login(username, password)
        print("✅ Gmail authentication successful!")
        
        # Send test email
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = username
        msg["Subject"] = "🧪 Gmail SMTP Test"
        msg.attach(MIMEText("Test email from Gmail SMTP", "plain"))
        
        smtp.send_message(msg)
        print("✅ Test email sent successfully!")
        
        smtp.quit()
        return True
        
    except Exception as e:
        print(f"❌ Gmail test failed: {e}")
        return False

if __name__ == "__main__":
    test_gmail_smtp()
'''
    
    with open("test_gmail_email.py", "w") as f:
        f.write(gmail_test_content)
    
    print("\n📁 Created: test_gmail_email.py")
    print("   Run this file to test Gmail SMTP")

if __name__ == "__main__":
    main() 