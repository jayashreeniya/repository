import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_zoho_in_config():
    """Test Zoho India server configuration"""
    print("🧪 Testing Zoho India Server Configuration")
    print("=" * 50)
    
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    server = os.getenv("SMTP_SERVER")
    port = int(os.getenv("SMTP_PORT", "465"))
    
    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Password length: {len(password) if password else 0}")
    
    # Test 1: SSL connection
    print(f"\n🔍 Test 1: SSL connection to {server}:{port}")
    try:
        smtp = smtplib.SMTP_SSL(server, port)
        print("✅ SSL connection successful")
        
        # Try login
        smtp.login(username, password)
        print("✅ Authentication successful!")
        
        # Send test email
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = username
        msg["Subject"] = "🧪 Test from Zoho India Server"
        msg.attach(MIMEText("This is a test email from Zoho India server", "plain"))
        
        smtp.send_message(msg)
        print("✅ Test email sent successfully!")
        
        smtp.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print(f"   Error code: {e.smtp_code}")
        print(f"   Error message: {e.smtp_error}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    # Test 2: TLS connection
    print(f"\n🔍 Test 2: TLS connection to {server}:587")
    try:
        smtp = smtplib.SMTP(server, 587)
        smtp.starttls()
        print("✅ TLS connection successful")
        
        # Try login
        smtp.login(username, password)
        print("✅ Authentication successful!")
        
        # Send test email
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = username
        msg["Subject"] = "🧪 Test from Zoho India Server (TLS)"
        msg.attach(MIMEText("This is a test email from Zoho India server using TLS", "plain"))
        
        smtp.send_message(msg)
        print("✅ Test email sent successfully!")
        
        smtp.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print(f"   Error code: {e.smtp_code}")
        print(f"   Error message: {e.smtp_error}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    return False

def check_zoho_in_requirements():
    """Check Zoho India specific requirements"""
    print("\n📋 Zoho India Server Requirements:")
    print("1. ✅ Server: smtp.zoho.in")
    print("2. ✅ Port: 465 (SSL) or 587 (TLS)")
    print("3. ✅ Username: Full email address")
    print("4. ❓ Password: App Password for India region")
    print("5. ❓ Account: Must be India region account")
    
    print("\n💡 Troubleshooting Tips:")
    print("- Make sure your Zoho account is in the India region")
    print("- Generate app password specifically for India server")
    print("- Check if your account supports SMTP")
    print("- Try both SSL (465) and TLS (587) ports")

if __name__ == "__main__":
    if test_zoho_in_config():
        print("\n🎉 Zoho India server authentication successful!")
        print("   Your email system is now working!")
    else:
        print("\n❌ Zoho India server authentication failed")
        check_zoho_in_requirements() 