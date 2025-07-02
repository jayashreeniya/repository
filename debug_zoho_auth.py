import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def test_different_auth_methods():
    """Test different authentication methods for Zoho"""
    print("🔍 Zoho SMTP Authentication Debug")
    print("=" * 40)
    
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Password type: {type(password)}")
    print(f"Password length: {len(password) if password else 0}")
    
    # Test 1: Basic SMTP_SSL
    print("\n🔍 Test 1: Basic SMTP_SSL")
    try:
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        server.login(username, password)
        print("✅ Basic SMTP_SSL authentication successful!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Basic SMTP_SSL failed: {e}")
    
    # Test 2: SMTP with TLS
    print("\n🔍 Test 2: SMTP with TLS")
    try:
        server = smtplib.SMTP("smtp.zoho.com", 587)
        server.starttls()
        server.login(username, password)
        print("✅ SMTP with TLS authentication successful!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP with TLS failed: {e}")
    
    # Test 3: Try with different password encoding
    print("\n🔍 Test 3: Password encoding test")
    try:
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        # Try with password as bytes
        server.login(username, password.encode('utf-8'))
        print("✅ Password as bytes authentication successful!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Password as bytes failed: {e}")
    
    # Test 4: Try with stripped password
    print("\n🔍 Test 4: Stripped password test")
    try:
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        stripped_password = password.strip()
        server.login(username, stripped_password)
        print("✅ Stripped password authentication successful!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Stripped password failed: {e}")
    
    return False

def check_zoho_requirements():
    """Check common Zoho SMTP requirements"""
    print("\n📋 Zoho SMTP Requirements Check:")
    print("1. ✅ SMTP server: smtp.zoho.com")
    print("2. ✅ Port: 465 (SSL) or 587 (TLS)")
    print("3. ✅ Username: Full email address")
    print("4. ❓ Password: App Password (not regular password)")
    print("5. ❓ Account: Must have SMTP access enabled")
    print("6. ❓ Two-factor: May need to be disabled or app password used")
    
    print("\n💡 Common Solutions:")
    print("- Generate a new App Password in Zoho settings")
    print("- Check if SMTP access is enabled in your Zoho account")
    print("- Try using port 587 with TLS instead of 465 with SSL")
    print("- Make sure your Zoho account supports SMTP (paid plans usually do)")

if __name__ == "__main__":
    if test_different_auth_methods():
        print("\n🎉 Authentication successful with one method!")
    else:
        print("\n❌ All authentication methods failed")
        check_zoho_requirements() 