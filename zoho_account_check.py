import os
from dotenv import load_dotenv

load_dotenv()

def check_zoho_account_info():
    """Check Zoho account information and requirements"""
    print("🔍 Zoho Account & SMTP Requirements Check")
    print("=" * 50)
    
    username = os.getenv("SMTP_USERNAME")
    print(f"Email: {username}")
    
    print("\n📋 Zoho Account Types & SMTP Access:")
    print("=" * 40)
    print("🆓 FREE ACCOUNT (Zoho Mail Free):")
    print("   - Limited to 5GB storage")
    print("   - SMTP access: ❌ Usually NOT available")
    print("   - POP3/IMAP: ✅ Available")
    print("   - Web interface only for sending")
    
    print("\n💳 PAID ACCOUNT (Zoho Mail Premium/Enterprise):")
    print("   - 5GB+ storage")
    print("   - SMTP access: ✅ Available")
    print("   - POP3/IMAP: ✅ Available")
    print("   - Full email client support")
    
    print("\n🔧 SMTP Authentication Requirements:")
    print("=" * 40)
    print("1. ✅ Account must support SMTP")
    print("2. ✅ App Password required (not regular password)")
    print("3. ✅ Two-factor authentication may need to be configured")
    print("4. ✅ SMTP access must be enabled in settings")
    
    print("\n💡 How to Check Your Account Type:")
    print("1. Log into https://mail.zoho.com")
    print("2. Go to Settings → Mail Accounts")
    print("3. Look for 'Account Type' or 'Plan'")
    print("4. Check if SMTP is mentioned in features")
    
    print("\n🔑 How to Generate App Password:")
    print("1. Go to Settings → Mail Accounts → Security")
    print("2. Look for 'App Passwords' or 'Two-Factor Authentication'")
    print("3. Generate new app password for 'SMTP'")
    print("4. Use this password in your .env file")
    
    print("\n⚠️  Common Issues:")
    print("- Free accounts don't support SMTP")
    print("- Regular password won't work for SMTP")
    print("- App password might be case-sensitive")
    print("- Account might need SMTP explicitly enabled")

def test_alternative_zoho_settings():
    """Test alternative Zoho SMTP settings"""
    print("\n🧪 Testing Alternative Zoho Settings")
    print("=" * 40)
    
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    
    # Test different Zoho SMTP servers
    servers = [
        ("smtp.zoho.com", 465, "SSL"),
        ("smtp.zoho.com", 587, "TLS"),
        ("smtp.zoho.eu", 465, "SSL (EU)"),
        ("smtp.zoho.eu", 587, "TLS (EU)"),
    ]
    
    import smtplib
    
    for server, port, description in servers:
        print(f"\n🔍 Testing {server}:{port} ({description})")
        try:
            if port == 465:
                smtp = smtplib.SMTP_SSL(server, port)
            else:
                smtp = smtplib.SMTP(server, port)
                smtp.starttls()
            
            smtp.login(username, password)
            print(f"✅ {description} authentication successful!")
            smtp.quit()
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ {description} authentication failed: {e}")
        except Exception as e:
            print(f"❌ {description} connection failed: {e}")
    
    return False

def main():
    """Run Zoho account check and alternative tests"""
    check_zoho_account_info()
    
    print("\n" + "=" * 50)
    print("Would you like to test alternative Zoho settings?")
    print("This will help identify if it's a server/port issue.")
    
    # Run alternative tests
    test_alternative_zoho_settings()

if __name__ == "__main__":
    main() 