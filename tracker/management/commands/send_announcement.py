"""
Management command to send announcement emails to all users.

Usage:
    python manage.py send_announcement
    python manage.py send_announcement --test user@example.com
"""

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Send announcement email to all users about new features'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            type=str,
            help='Send test email to specific address instead of all users',
        )
        parser.add_argument(
            '--subject',
            type=str,
            default='🎉 New Features in Pushup Counter!',
            help='Email subject line',
        )
    
    def handle(self, *args, **options):
        test_email = options.get('test')
        subject = options['subject']
        
        # Email content
        text_content = self.get_text_content()
        html_content = self.get_html_content()
        
        if test_email:
            # Send test email to single recipient
            self.stdout.write(self.style.WARNING(f'📧 Sending TEST email to: {test_email}'))
            self.send_email(subject, text_content, html_content, [test_email])
            self.stdout.write(self.style.SUCCESS('✅ Test email sent!'))
        else:
            # Send to all active users with email addresses
            users = User.objects.filter(is_active=True).exclude(email='')
            
            if not users.exists():
                self.stdout.write(self.style.ERROR('❌ No users found with email addresses'))
                return
            
            self.stdout.write(self.style.WARNING(f'📧 Sending announcement to {users.count()} users...'))
            
            sent_count = 0
            failed_count = 0
            
            for user in users:
                try:
                    self.send_email(subject, text_content, html_content, [user.email])
                    sent_count += 1
                    self.stdout.write(f'  ✅ Sent to {user.username} ({user.email})')
                except Exception as e:
                    failed_count += 1
                    self.stdout.write(self.style.ERROR(f'  ❌ Failed for {user.username}: {e}'))
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'📊 Summary:'))
            self.stdout.write(self.style.SUCCESS(f'   ✅ Successfully sent: {sent_count}'))
            if failed_count > 0:
                self.stdout.write(self.style.ERROR(f'   ❌ Failed: {failed_count}'))
    
    def send_email(self, subject, text_content, html_content, recipients):
        """Send email to recipients."""
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
    
    def get_text_content(self):
        """Plain text version of the email."""
        return """
Hi there! 👋

Great news! We've just rolled out some exciting updates to the Pushup Counter app based on your feedback:

🎯 NEW FEATURES:

• Floating Add Button (Mobile) - No more scrolling! A convenient "+" button now floats at the bottom-right of your screen on mobile, making it super easy to log your pushups instantly.

• History Totals - When viewing your history, you now see the total pushups for any filtered period (month/year or all time).

• Lifetime Total - Your dashboard now shows your all-time pushup total alongside your monthly stats. Track your long-term progress!

• Full Names Display - Competition winners and activity feeds now show real names instead of usernames for a more personal touch.

🐛 BUG FIXES:

• Fixed Date Display - "Today's Pushups" now shows the correct day (no more timezone confusion!).

• Better Stat Labels - All dashboard stats clearly indicate if they're for "This Month" or "All Time".

• Competition Winners - October competition winner is now properly displayed with their total pushups.

• Auto Winner Calculation - When a competition ends, the winner is now automatically determined.

💡 HOW TO USE:

1. On mobile: Look for the purple "+" button at the bottom-right corner
2. Visit your History page to see filtered totals
3. Check your dashboard for your lifetime achievement total
4. View past competition winners with their full details

Try out these new features and let us know what you think!

Keep pushing! 💪

---
Pushup Counter Team
https://asavoiu.pythonanywhere.com
        """.strip()
    
    def get_html_content(self):
        """HTML version of the email."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }
        .content {
            padding: 30px 20px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #667eea;
            font-size: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .feature {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
        }
        .feature h3 {
            margin: 0 0 8px 0;
            color: #333;
            font-size: 16px;
        }
        .feature p {
            margin: 0;
            color: #666;
            font-size: 14px;
        }
        .bug-fix {
            border-left-color: #10b981;
        }
        .cta {
            text-align: center;
            margin: 30px 0;
        }
        .button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
        }
        .tips {
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }
        .tips h3 {
            margin: 0 0 10px 0;
            color: #856404;
        }
        .tips ul {
            margin: 0;
            padding-left: 20px;
        }
        .tips li {
            color: #856404;
            margin-bottom: 5px;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
        .emoji {
            font-size: 24px;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 New Features Are Here!</h1>
            <p>We've made some exciting improvements based on your feedback</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2><span class="emoji">🎯</span> New Features</h2>
                
                <div class="feature">
                    <h3>📱 Floating Add Button (Mobile)</h3>
                    <p>No more scrolling! A convenient "+" button now floats at the bottom-right of your screen on mobile, making it super easy to log your pushups instantly.</p>
                </div>
                
                <div class="feature">
                    <h3>📊 History Totals</h3>
                    <p>When viewing your history, you now see the total pushups for any filtered period (month/year or all time). Perfect for tracking specific goals!</p>
                </div>
                
                <div class="feature">
                    <h3>♾️ Lifetime Total</h3>
                    <p>Your dashboard now shows your all-time pushup total alongside your monthly stats. Celebrate your long-term achievements!</p>
                </div>
                
                <div class="feature">
                    <h3>👤 Full Names Display</h3>
                    <p>Competition winners and activity feeds now show real names instead of usernames for a more personal and friendly experience.</p>
                </div>
            </div>
            
            <div class="section">
                <h2><span class="emoji">🐛</span> Bug Fixes</h2>
                
                <div class="feature bug-fix">
                    <h3>✅ Fixed Date Display</h3>
                    <p>"Today's Pushups" now shows the correct day (no more timezone confusion!).</p>
                </div>
                
                <div class="feature bug-fix">
                    <h3>✅ Better Stat Labels</h3>
                    <p>All dashboard stats clearly indicate if they're for "This Month" or "All Time".</p>
                </div>
                
                <div class="feature bug-fix">
                    <h3>✅ Competition Winners</h3>
                    <p>October competition winner is now properly displayed with their total pushups.</p>
                </div>
                
                <div class="feature bug-fix">
                    <h3>✅ Auto Winner Calculation</h3>
                    <p>When a competition ends, the winner is now automatically determined and displayed.</p>
                </div>
            </div>
            
            <div class="section">
                <div class="tips">
                    <h3>💡 How to Use These Features</h3>
                    <ul>
                        <li>On mobile: Look for the purple "+" button at the bottom-right corner</li>
                        <li>Visit your History page to see filtered totals</li>
                        <li>Check your dashboard for your lifetime achievement total</li>
                        <li>View past competition winners with their full details</li>
                    </ul>
                </div>
            </div>
            
            <div class="cta">
                <a href="https://asavoiu.pythonanywhere.com" class="button">
                    Open Pushup Counter
                </a>
            </div>
            
            <p style="text-align: center; color: #666;">
                Try out these new features and keep crushing your goals! 💪
            </p>
        </div>
        
        <div class="footer">
            <p>This email was sent from Pushup Counter</p>
            <p><a href="https://asavoiu.pythonanywhere.com" style="color: #667eea;">asavoiu.pythonanywhere.com</a></p>
            <p style="margin-top: 10px;">Keep pushing! 💪</p>
        </div>
    </div>
</body>
</html>
        """.strip()

