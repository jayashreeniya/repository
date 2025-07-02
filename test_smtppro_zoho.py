import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_smtppro_zoho():
    """Test smtppro.zoho.in configuration"""
    print("🧪 Testing smtppro.zoho.in Configuration")
    print("=" * 50)
    
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    server = os.getenv("SMTP_SERVER")
    port = int(os.getenv("SMTP_PORT", "587"))
    
    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Password length: {len(password) if password else 0}")
    
    # Test TLS connection (port 587)
    print(f"\n🔍 Testing TLS connection to {server}:{port}")
    try:
        smtp = smtplib.SMTP(server, port)
        print("✅ Connected to SMTP server")
        
        smtp.starttls()
        print("✅ TLS started successfully")
        
        # Try authentication
        smtp.login(username, password)
        print("✅ Authentication successful!")
        
        # Send test email
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = username
        msg["Subject"] = "🧪 Test from smtppro.zoho.in"
        msg.attach(MIMEText("This is a test email from smtppro.zoho.in server", "plain"))
        
        smtp.send_message(msg)
        print("✅ Test email sent successfully!")
        
        smtp.quit()
        
        print(f"\n🎉 SUCCESS! smtppro.zoho.in is working!")
        print("   Your email system is now ready!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print(f"   Error code: {e.smtp_code}")
        print(f"   Error message: {e.smtp_error}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    # Test SSL connection (port 465) as fallback
    print(f"\n🔍 Testing SSL connection to {server}:465")
    try:
        smtp = smtplib.SMTP_SSL(server, 465)
        print("✅ Connected to SMTP server (SSL)")
        
        # Try authentication
        smtp.login(username, password)
        print("✅ Authentication successful!")
        
        # Send test email
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = username
        msg["Subject"] = "🧪 Test from smtppro.zoho.in (SSL)"
        msg.attach(MIMEText("This is a test email from smtppro.zoho.in server using SSL", "plain"))
        
        smtp.send_message(msg)
        print("✅ Test email sent successfully!")
        
        smtp.quit()
        
        print(f"\n🎉 SUCCESS! smtppro.zoho.in with SSL is working!")
        print("   Your email system is now ready!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print(f"   Error code: {e.smtp_code}")
        print(f"   Error message: {e.smtp_error}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    return False

if __name__ == "__main__":
    if test_smtppro_zoho():
        print("\n🎉 smtppro.zoho.in authentication successful!")
        print("   Your email system is now working!")
        print("   You can run: python niya_agent.py")
    else:
        print("\n❌ smtppro.zoho.in authentication failed")
        print("   Consider switching to Gmail SMTP") 