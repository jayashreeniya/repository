import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_smtp_config(server, port, use_ssl=True, use_tls=False):
    """Test a specific SMTP configuration"""
    print(f"\n🔍 Testing: {server}:{port} (SSL: {use_ssl}, TLS: {use_tls})")
    
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    try:
        if use_ssl:
            server_conn = smtplib.SMTP_SSL(server, port)
        else:
            server_conn = smtplib.SMTP(server, port)
            if use_tls:
                server_conn.starttls()
        
        print(f"✅ Connected to {server}:{port}")
        
        # Try to login
        server_conn.login(smtp_username, smtp_password)
        print("✅ Authentication successful!")
        
        # Try to send a test email
        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = smtp_username
        msg["Subject"] = f"Test from {server}:{port}"
        msg.attach(MIMEText("Test email", "plain"))
        
        server_conn.sendmail(smtp_username, smtp_username, msg.as_string())
        print("✅ Email sent successfully!")
        
        server_conn.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    """Test different Zoho SMTP configurations"""
    print("🔧 Zoho SMTP Configuration Test")
    print("=" * 50)
    
    # Common Zoho SMTP configurations
    configs = [
        ("smtp.zoho.com", 465, True, False),   # SSL
        ("smtp.zoho.com", 587, False, True),   # TLS
        ("smtp.zoho.com", 587, False, False),  # No encryption
        ("smtp.zoho.eu", 465, True, False),    # EU server SSL
        ("smtp.zoho.eu", 587, False, True),    # EU server TLS
    ]
    
    working_configs = []
    
    for server, port, use_ssl, use_tls in configs:
        if test_smtp_config(server, port, use_ssl, use_tls):
            working_configs.append((server, port, use_ssl, use_tls))
    
    print(f"\n📊 Results: {len(working_configs)}/{len(configs)} configurations worked")
    
    if working_configs:
        print("\n✅ Working configurations:")
        for server, port, use_ssl, use_tls in working_configs:
            encryption = "SSL" if use_ssl else "TLS" if use_tls else "None"
            print(f"   - {server}:{port} ({encryption})")
        
        # Suggest the best configuration
        best_config = working_configs[0]
        print(f"\n💡 Recommended configuration:")
        print(f"   SMTP_SERVER={best_config[0]}")
        print(f"   SMTP_PORT={best_config[1]}")
        if best_config[2]:  # SSL
            print("   (Use SSL)")
        elif best_config[3]:  # TLS
            print("   (Use TLS)")
    else:
        print("\n❌ No working configurations found.")
        print("   Please check:")
        print("   1. Your Zoho username and password")
        print("   2. Whether you need an App Password")
        print("   3. Your Zoho account settings")

if __name__ == "__main__":
    main() 