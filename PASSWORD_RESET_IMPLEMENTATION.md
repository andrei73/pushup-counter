# 🔐 Password Reset Implementation

## ✅ What's Been Implemented

### 1. Email Configuration
- Gmail SMTP integration (port 587 with TLS)
- Environment variable setup for security
- Test script (`test_email.py`) to verify email functionality

### 2. Password Reset Flow
Complete 4-step password reset process:

1. **Request Reset** (`/password-reset/`)
   - User enters their email address
   - System sends password reset email

2. **Email Sent Confirmation** (`/password-reset/done/`)
   - Confirms email was sent
   - Shows helpful tips if email not received

3. **Set New Password** (`/password-reset-confirm/<uidb64>/<token>/`)
   - User clicks link in email
   - Enters new password (with validation)
   - Link expires after 24 hours
   - Link can only be used once

4. **Reset Complete** (`/password-reset-complete/`)
   - Confirms password was changed
   - Provides login link

### 3. User Interface
- "Forgot your password?" link added to login page
- All templates styled with Bootstrap 5 to match app design
- Responsive and mobile-friendly
- Clear error messages and helpful instructions

### 4. Email Template
- Custom branded email content
- Clear reset link
- Security instructions
- 24-hour expiration notice

---

## 🧪 Testing Password Reset

### Local Development (With VPN Off)

1. **Start the development server:**
```bash
cd /Users/asavoiu/Workspace/Dev_Projects/fitCounter

# Set email credentials
export EMAIL_HOST_USER="andrei.savoiu@gmail.com"
export EMAIL_HOST_PASSWORD="uvwhmfzuclyjxcuq"

# Run server
python manage.py runserver
```

2. **Test the flow:**
- Go to: http://127.0.0.1:8000/login/
- Click "Forgot your password?"
- Enter your email address
- Check your inbox for the reset email
- Click the link in the email
- Enter your new password
- Login with new password

### Important Notes

⚠️ **VPN:** Make sure your VPN is OFF when testing email - corporate VPNs often block SMTP ports.

⚠️ **Spam Folder:** Password reset emails might land in spam. Check there if you don't see the email.

⏱️ **Link Expiration:** Reset links expire after 24 hours for security.

🔒 **One-Time Use:** Each reset link can only be used once.

---

## 🚀 Production Setup (PythonAnywhere)

### Step 1: Update wsgi.py

Add email configuration to `/var/www/asavoiu_pythonanywhere_com_wsgi.py`:

```python
# Email settings
os.environ['EMAIL_HOST_USER'] = 'andrei.savoiu@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'uvwhmfzuclyjxcuq'
```

### Step 2: Deploy Changes

```bash
# On PythonAnywhere console:
cd ~/pushupCounter

# Pull latest changes
git pull origin develop

# Reload web app
# (Use the "Reload" button on PythonAnywhere Web tab)
```

### Step 3: Test on Production

- Go to: https://asavoiu.pythonanywhere.com/password-reset/
- Test the complete flow

---

## 📧 Email Settings Reference

### Current Configuration (settings.py)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', 'noreply@pushupapp.com')
SERVER_EMAIL = os.environ.get('EMAIL_HOST_USER', 'noreply@pushupapp.com')
```

### Email Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `EMAIL_HOST_USER` | `andrei.savoiu@gmail.com` | Gmail account |
| `EMAIL_HOST_PASSWORD` | `uvwhmfzuclyjxcuq` | 16-char App Password |

**Security:** These should NEVER be committed to git. Always use environment variables.

---

## 🔧 Troubleshooting

### Issue: "Connection reset by peer" or timeout

**Solution:** Disable VPN. Corporate VPNs often block SMTP ports 587/465.

### Issue: Email not received

**Solutions:**
1. Check spam folder
2. Wait a few minutes (delivery can be delayed)
3. Verify email address is correct
4. Check Django server logs for errors

### Issue: "Invalid reset link"

**Causes:**
- Link expired (>24 hours old)
- Link already used
- Link was malformed (copy/paste issue)

**Solution:** Request a new reset link

### Issue: "SMTPAuthenticationError"

**Causes:**
- Wrong App Password
- 2FA not enabled on Google account
- Email address incorrect

**Solution:** 
1. Regenerate App Password at: https://myaccount.google.com/apppasswords
2. Verify 2FA is enabled on your Google account
3. Double-check email address

---

## 📋 Files Modified/Created

### New Templates Created:
- `tracker/templates/tracker/password_reset_form.html`
- `tracker/templates/tracker/password_reset_done.html`
- `tracker/templates/tracker/password_reset_confirm.html`
- `tracker/templates/tracker/password_reset_complete.html`
- `tracker/templates/tracker/password_reset_email.html`
- `tracker/templates/tracker/password_reset_subject.txt`

### Modified Files:
- `tracker/urls.py` - Added password reset URLs
- `tracker/templates/tracker/login.html` - Added "Forgot Password?" link
- `pushup_counter/settings.py` - Added email configuration

### Helper Files:
- `test_email.py` - Email testing script
- `EMAIL_SETUP.md` - Email configuration guide

---

## 🎯 What's Next?

Password reset is complete! ✅

Other features you might want to add:

1. **Email Verification on Signup**
   - Send verification email when users register
   - Prevent unverified users from logging in

2. **Welcome Email**
   - Send welcome email to new users
   - Include getting started tips

3. **Competition Notifications**
   - Email when competition ends
   - Notify winner
   - Send reminders

4. **Password Change (from profile)**
   - Allow logged-in users to change password
   - Without needing email reset

5. **Two-Factor Authentication (2FA)**
   - Extra security layer
   - SMS or authenticator app

Let me know which feature you'd like to tackle next! 😊

