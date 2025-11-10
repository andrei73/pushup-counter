# 📧 Sending Announcement Emails to Users

## Overview

You can now easily send announcement emails to all users about new features, bug fixes, or any other updates using the `send_announcement` management command.

---

## 🚀 Quick Start

### Step 1: Test the Email (Recommended)

**Always test first** by sending to your own email:

```bash
# Local
cd /Users/asavoiu/Workspace/Dev_Projects/fitCounter
source venv/bin/activate
export EMAIL_HOST_USER="andrei.savoiu@gmail.com"
export EMAIL_HOST_PASSWORD="uvwhmfzuclyjxcuq"
python manage.py send_announcement --test your.email@example.com

# PythonAnywhere
cd ~/pushupCounter
workon pushupenv
python manage.py send_announcement --test andrei.savoiu@gmail.com
```

**Check your inbox** to see how the email looks!

---

### Step 2: Send to All Users

Once you're happy with the test email:

```bash
# PythonAnywhere
cd ~/pushupCounter
workon pushupenv
python manage.py send_announcement
```

**Output:**
```
📧 Sending announcement to 5 users...
  ✅ Sent to john_doe (john@example.com)
  ✅ Sent to jane_smith (jane@example.com)
  ✅ Sent to alex_jones (alex@example.com)
  ...

📊 Summary:
   ✅ Successfully sent: 5
```

---

## 📝 Command Options

### Basic Usage

```bash
# Send to all users with default subject
python manage.py send_announcement
```

### Send Test Email

```bash
# Send to a specific email address (test first!)
python manage.py send_announcement --test your.email@example.com
```

### Custom Subject Line

```bash
# Use a custom subject
python manage.py send_announcement --subject "Check out our new mobile features! 📱"
```

### Combined Options

```bash
# Test with custom subject
python manage.py send_announcement --test your.email@example.com --subject "🎉 New Features!"
```

---

## ✉️ What Gets Sent

The command sends a beautifully formatted email with:

### ✅ Features Announced:
- 📱 Floating Add Button (Mobile)
- 📊 History Totals
- ♾️ Lifetime Total
- 👤 Full Names Display

### ✅ Bug Fixes Announced:
- Fixed Date Display (Timezone)
- Better Stat Labels
- Competition Winners Display
- Auto Winner Calculation

### ✅ Email Includes:
- **HTML version** - Beautiful gradient header, styled sections, call-to-action button
- **Plain text version** - For email clients that don't support HTML
- **Mobile responsive** - Looks great on all devices
- **Direct link** to your app

---

## 🎨 Email Preview

### Header
```
╔═══════════════════════════════════════════╗
║    🎉 New Features Are Here!              ║
║    We've made exciting improvements       ║
║    based on your feedback                 ║
╚═══════════════════════════════════════════╝
```

### Content Sections
- **New Features** (4 feature cards with descriptions)
- **Bug Fixes** (4 bug fix cards with descriptions)
- **How to Use** (Quick tips box)
- **Call to Action** (Button to open the app)

### Footer
- App link
- Motivational message

---

## 🎯 Who Receives the Email?

The command sends to:
- ✅ All **active users** (`is_active=True`)
- ✅ Who have an **email address** set
- ❌ Inactive users are skipped
- ❌ Users without email addresses are skipped

---

## 📊 Understanding the Output

```bash
📧 Sending announcement to 10 users...
  ✅ Sent to user1 (user1@example.com)    # Success
  ✅ Sent to user2 (user2@example.com)    # Success
  ❌ Failed for user3: [Errno 111]         # Failed (shows error)
  ✅ Sent to user4 (user4@example.com)    # Success

📊 Summary:
   ✅ Successfully sent: 9
   ❌ Failed: 1
```

---

## 🔧 Customizing the Email Content

### Edit the Announcement

To change the email content:

1. Open `tracker/management/commands/send_announcement.py`
2. Edit the `get_text_content()` method (plain text version)
3. Edit the `get_html_content()` method (HTML version)
4. Save and run the command

### Example: Add a New Feature

In `get_html_content()`, add a new feature card:

```html
<div class="feature">
    <h3>🎯 Your New Feature</h3>
    <p>Description of your awesome new feature goes here!</p>
</div>
```

In `get_text_content()`, add the same info:

```
• Your New Feature - Description of your awesome new feature goes here!
```

---

## 🚀 Deployment Workflow

### Before Sending:

1. **Deploy your changes** to PythonAnywhere
   ```bash
   git push origin develop
   # Then on PythonAnywhere: git pull origin develop
   ```

2. **Test the features** yourself
   - Make sure everything works as expected

3. **Send test email** to yourself
   ```bash
   python manage.py send_announcement --test your.email@example.com
   ```

4. **Review the test email**
   - Check formatting
   - Verify all links work
   - Test on mobile device

5. **Send to all users**
   ```bash
   python manage.py send_announcement
   ```

---

## 💡 Best Practices

### ✅ DO:
- Always send a test email first
- Review the test email on both desktop and mobile
- Send during business hours (users are more likely to read)
- Keep announcements concise and focused
- Include clear call-to-action
- Test all links before sending

### ❌ DON'T:
- Send too frequently (max once per week)
- Send without testing first
- Include broken links or images
- Use all caps or excessive exclamation marks
- Send during late night/early morning hours

---

## 🔐 Gmail App Password

The emails are sent using your Gmail account:

- **Email:** `andrei.savoiu@gmail.com`
- **App Password:** `uvwhmfzuclyjxcuq`

**Note:** This is an "App Password" (not your regular Gmail password), which is more secure for automated sending.

### Gmail Limits:
- **500 emails per day** for regular Gmail accounts
- If you have more users, consider using a dedicated email service like:
  - SendGrid
  - Mailgun
  - Amazon SES
  - Mailchimp

---

## 🐛 Troubleshooting

### Error: "No users found with email addresses"

**Problem:** No users have email addresses set.

**Solution:** Users need to provide their email during signup, or you can add them manually in the admin.

---

### Error: "SMTP Authentication failed"

**Problem:** Email credentials are wrong or not set.

**Solution:** 
```bash
# Set environment variables
export EMAIL_HOST_USER="andrei.savoiu@gmail.com"
export EMAIL_HOST_PASSWORD="uvwhmfzuclyjxcuq"
```

---

### Error: "[Errno 111] Connection refused"

**Problem:** Can't connect to Gmail SMTP server.

**Solution:** Check your internet connection or VPN. Gmail SMTP might be blocked.

---

### Emails Not Arriving

**Check:**
1. Spam/Junk folder
2. Gmail "Sent" folder to verify it was sent
3. Email address is correct
4. User's inbox isn't full

---

## 📋 Example Scenarios

### Scenario 1: New Feature Release

```bash
# Test first
python manage.py send_announcement --test andrei.savoiu@gmail.com

# Check inbox, verify it looks good

# Send to everyone
python manage.py send_announcement
```

---

### Scenario 2: Bug Fix Notification

Edit the command to focus on bug fixes:

```bash
python manage.py send_announcement --subject "🐛 Bug Fixes: Improved App Experience"
```

---

### Scenario 3: Competition Announcement

```bash
python manage.py send_announcement --subject "🏆 November Competition Starts Today!"
```

---

## 🎓 Advanced: Creating Custom Announcements

You can create multiple announcement commands for different purposes:

### Example: Weekly Summary Command

Create `tracker/management/commands/send_weekly_summary.py`:

```python
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
# ... implement weekly summary logic
```

Usage:
```bash
python manage.py send_weekly_summary
```

### Example: Winner Notification Command

Create `tracker/management/commands/notify_winner.py`:

```python
from django.core.management.base import BaseCommand
# ... implement winner notification logic
```

---

## 📊 Monitoring Email Success

### Track in Logs

Add logging to the command:

```python
import logging
logger = logging.getLogger(__name__)

# In send_email method:
logger.info(f"Email sent to {recipients}")
```

### Gmail Sent Folder

Check your Gmail "Sent" folder to see all sent emails.

---

## ✨ Summary

**Quick Reference:**

| Task | Command |
|------|---------|
| **Test email** | `python manage.py send_announcement --test your@email.com` |
| **Send to all** | `python manage.py send_announcement` |
| **Custom subject** | `python manage.py send_announcement --subject "Your Subject"` |
| **Edit content** | Edit `send_announcement.py` |

**Remember:**
1. ✅ Always test first
2. ✅ Review on mobile and desktop
3. ✅ Send during business hours
4. ✅ Keep it concise and actionable

Happy announcing! 📧💪

