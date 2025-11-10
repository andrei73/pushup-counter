#!/usr/bin/env python
"""Test email sending - Run with: python manage.py shell < send_test_email.py"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"Email Host: {settings.EMAIL_HOST}")
print(f"Email Port: {settings.EMAIL_PORT}")
print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
print(f"Email From: {settings.EMAIL_HOST_USER}")
print(f"Password Set: {'Yes' if settings.EMAIL_HOST_PASSWORD else 'No'}")
print()

# Ask for recipient
recipient = input("Enter recipient email address: ")

# Test 1: Simple text email
print("\n📧 Sending simple text email...")
try:
    send_mail(
        subject='Test Email from Pushup Counter',
        message='This is a simple test email. If you receive this, email is working! 💪',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
        fail_silently=False,
    )
    print("✅ Simple email sent successfully!")
except Exception as e:
    print(f"❌ Error sending simple email: {e}")

# Test 2: HTML email
print("\n📧 Sending HTML email...")
try:
    subject = '🏆 Pushup Counter - HTML Email Test'
    text_content = 'This is the plain text version.'
    html_content = '''
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; }
            .stats { background: #f3f4f6; padding: 15px; border-radius: 10px; margin: 20px 0; }
            .button { background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💪 Pushup Counter</h1>
            <p>HTML Email Test</p>
        </div>
        <div class="content">
            <h2>Email is Working!</h2>
            <p>If you're reading this, the HTML email functionality is working correctly.</p>
            
            <div class="stats">
                <h3>📊 Sample Stats</h3>
                <ul>
                    <li>Today's Pushups: 50</li>
                    <li>This Month: 1,234</li>
                    <li>Lifetime Total: 5,000</li>
                </ul>
            </div>
            
            <p>
                <a href="https://asavoiu.pythonanywhere.com" class="button">
                    Visit Pushup Counter
                </a>
            </p>
            
            <p style="color: #666; font-size: 12px; margin-top: 40px;">
                This is an automated test email from Pushup Counter.
            </p>
        </div>
    </body>
    </html>
    '''
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    print("✅ HTML email sent successfully!")
except Exception as e:
    print(f"❌ Error sending HTML email: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("Check your inbox for two test emails:")
print("1. Simple text email")
print("2. Styled HTML email")
print()

