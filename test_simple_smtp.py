import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def test_simple_smtp():
    """Simple SMTP test with detailed error reporting"""
    print("🧪 Simple SMTP Test")
    print("=" * 30)
    
    # Get credentials
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Password length: {len(password) if password else 0}")
    
    try:
        # Connect to Zoho SMTP
        print("\n🔗 Connecting to smtp.zoho.com:465...")
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        print("✅ Connected successfully")
        
        # Try to login
        print(f"\n🔐 Attempting login with {username}...")
        server.login(username, password)
        print("✅ Login successful!")
        
        # Send a simple test email
        print("\n📧 Sending test email...")
        msg = MIMEText("This is a test email from Niya Sales Agent")
        msg['Subject'] = "Test Email"
        msg['From'] = username
        msg['To'] = username
        
        server.send_message(msg)
        print("✅ Email sent successfully!")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication Error: {e}")
        print(f"   Error code: {e.smtp_code}")
        print(f"   Error message: {e.smtp_error}")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    test_simple_smtp() 