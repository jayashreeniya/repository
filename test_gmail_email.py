import os
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
