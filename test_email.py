#!/usr/bin/env python
"""
Quick email test script for Pushup Counter app
Run this after setting up email environment variables
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pushup_counter.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_email():
    """Test email configuration by sending a test email"""
    
    print("=" * 60)
    print("🧪 Testing Email Configuration")
    print("=" * 60)
    
    # Check if email settings are configured
    if not settings.EMAIL_HOST_USER:
        print("❌ ERROR: EMAIL_HOST_USER is not set!")
        print("\nPlease set environment variables:")
        print('  export EMAIL_HOST_USER="your-email@gmail.com"')
        print('  export EMAIL_HOST_PASSWORD="your-app-password"')
        return
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("❌ ERROR: EMAIL_HOST_PASSWORD is not set!")
        print("\nPlease set environment variables:")
        print('  export EMAIL_HOST_USER="your-email@gmail.com"')
        print('  export EMAIL_HOST_PASSWORD="your-app-password"')
        return
    
    print(f"✅ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"✅ EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"✅ EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"✅ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print()
    
    # Get recipient email
    recipient = input(f"Enter recipient email (press Enter to send to {settings.EMAIL_HOST_USER}): ").strip()
    if not recipient:
        recipient = settings.EMAIL_HOST_USER
    
    print(f"\n📧 Sending test email to: {recipient}")
    print("⏳ Please wait...")
    
    try:
        send_mail(
            subject='🏋️ Test Email from Pushup Counter App',
            message='Congratulations! Your email configuration is working correctly.\n\nYou can now use password reset and email notifications.\n\n💪 Keep pushing!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Email sent successfully!")
        print("=" * 60)
        print(f"\n📬 Check your inbox at: {recipient}")
        print("💡 Don't forget to check your spam folder if you don't see it.")
        print("\n🎉 Your email configuration is working correctly!")
        print("\nNext steps:")
        print("  1. Implement password reset")
        print("  2. Add email notifications (optional)")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR: Failed to send email")
        print("=" * 60)
        print(f"\nError details: {e}")
        print("\nCommon solutions:")
        print("  1. Make sure you're using the App Password, not your regular password")
        print("  2. Check that 2-Factor Authentication is enabled on your Google account")
        print("  3. Verify your Gmail address is correct")
        print("  4. Check your internet connection")
        print("\nSee EMAIL_SETUP.md for more troubleshooting tips.")


if __name__ == '__main__':
    test_email()

