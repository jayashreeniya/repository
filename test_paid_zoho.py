import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_paid_zoho_configs():
    """Test all possible configurations for paid Zoho account"""
    print("🧪 Testing Paid Zoho Account - All Configurations")
    print("=" * 60)
    
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    
    # All possible Zoho configurations for paid accounts
    configs = [
        ("smtppro.zoho.in", 587, "TLS"),
        ("smtppro.zoho.in", 465, "SSL"),
        ("smtp.zoho.in", 587, "TLS"),
        ("smtp.zoho.in", 465, "SSL"),
        ("smtp.zoho.com", 587, "TLS"),
        ("smtp.zoho.com", 465, "SSL"),
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
            msg["Subject"] = f"🧪 Paid Zoho Test - {server}:{port}"
            msg.attach(MIMEText(f"Test email from paid Zoho account using {server}:{port}", "plain"))
            
            smtp.send_message(msg)
            print("✅ Email sent successfully!")
            
            smtp.quit()
            
            print(f"\n🎉 SUCCESS! Working configuration found:")
            print(f"   SMTP_SERVER={server}")
            print(f"   SMTP_PORT={port}")
            print(f"   Encryption: {encryption}")
            
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    return False

def check_paid_zoho_requirements():
    """Check requirements for paid Zoho account"""
    print("\n📋 Paid Zoho Account Requirements:")
    print("1. ✅ Paid Zoho Mail account")
    print("2. ✅ SMTP access enabled")
    print("3. ❓ App Password generated for SMTP")
    print("4. ❓ Account region matches server")
    
    print("\n💡 Troubleshooting for Paid Accounts:")
    print("- Generate a new App Password specifically for SMTP")
    print("- Make sure SMTP access is enabled in account settings")
    print("- Check if your account is in the correct region")
    print("- Try using your regular password instead of app password")
    print("- Contact Zoho support if issues persist")

def test_with_regular_password():
    """Test with regular password (sometimes works for paid accounts)"""
    print("\n🔍 Testing with regular password...")
    print("Note: This is less secure but sometimes works with paid accounts")
    
    # You would need to manually enter your regular password here
    # For security reasons, I won't include it in the code
    print("To test with regular password:")
    print("1. Temporarily replace SMTP_PASSWORD in .env with your regular password")
    print("2. Run this test again")
    print("3. Remember to change back to app password after testing")

if __name__ == "__main__":
    if test_paid_zoho_configs():
        print("\n🎉 Paid Zoho account is working!")
        print("   Your email system is ready for production use.")
        print("   Run: python niya_agent.py")
    else:
        print("\n❌ All paid Zoho configurations failed")
        check_paid_zoho_requirements()
        test_with_regular_password()
        
        print("\n💡 Next Steps:")
        print("1. Generate a new App Password in Zoho settings")
        print("2. Make sure SMTP access is enabled")
        print("3. Try with regular password temporarily")
        print("4. Consider switching to Gmail if issues persist") 