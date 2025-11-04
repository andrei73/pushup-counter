# 📧 Email Setup Guide

## Local Development Setup

### Step 1: Set Environment Variables

**Option A: Export in Terminal (Temporary - good for testing)**

```bash
# In your terminal, before running Django:
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"

# Then run your Django server:
python manage.py runserver
```

**Option B: Create .env file (Better - persists across sessions)**

1. Install python-decouple:
```bash
pip install python-decouple
```

2. Create `.env` file in project root:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

3. Update `settings.py` to use decouple (optional - current setup works with export)

**Option C: Set in your IDE/Editor**

If using VSCode or PyCharm, you can set environment variables in your run configuration.

---

## PythonAnywhere Production Setup

**Add to your `wsgi.py` file:**

```python
# Email settings
os.environ['EMAIL_HOST_USER'] = 'your-email@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'your-16-char-app-password'
```

**Important:** Keep your App Password secret! Never commit it to git.

---

## Testing Email Configuration

### Test 1: Django Shell Test

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email from Pushup App',
    'If you receive this, email is working!',
    'your-email@gmail.com',  # From
    ['your-email@gmail.com'],  # To (send to yourself)
    fail_silently=False,
)
```

If you see no errors and receive the email, it's working! ✅

### Test 2: Password Reset Test

1. Go to `/accounts/password-reset/`
2. Enter your email
3. Check your inbox for reset link
4. Click link and reset password

---

## Common Issues

### Issue: "SMTPAuthenticationError: Username and Password not accepted"

**Solutions:**
- Make sure you're using the **App Password**, not your regular Gmail password
- Check that 2-Factor Authentication is enabled on your Google account
- Verify EMAIL_HOST_USER is your full Gmail address (e.g., `example@gmail.com`)
- Make sure there are no spaces in your App Password (Django handles spaces automatically, but best to remove them)

### Issue: "SMTPServerDisconnected: Connection unexpectedly closed"

**Solutions:**
- Check your internet connection
- Try again (Gmail sometimes rate-limits)
- Verify EMAIL_PORT=587 and EMAIL_USE_TLS=True

### Issue: Email not received

**Solutions:**
- Check spam folder
- Verify recipient email is correct
- Check Django logs for errors
- Try sending to a different email address

---

## Gmail App Password Setup

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Google account
3. Select "Mail" as the app
4. Select "Other (Custom name)" as the device → type "Django App"
5. Click "Generate"
6. Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)
7. Use this password in EMAIL_HOST_PASSWORD

**Note:** You can only see this password once. If you lose it, delete and create a new one.

---

## Security Notes

✅ **DO:**
- Use environment variables
- Keep App Password secret
- Use different credentials for development/production
- Revoke App Password if compromised

❌ **DON'T:**
- Commit credentials to git
- Share your App Password
- Use your regular Gmail password
- Hard-code credentials in settings.py

---

## Switching to SendGrid (Optional - for production)

If you need better deliverability or higher volume:

1. Sign up at: https://sendgrid.com
2. Verify your email
3. Create API key
4. Update settings.py:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # This is literal 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY', '')
```

5. Set environment variable:
```bash
export SENDGRID_API_KEY="your-sendgrid-api-key"
```

**SendGrid Benefits:**
- Better deliverability (less likely to go to spam)
- Email analytics
- 100 emails/day free forever
- Professional sender reputation

---

## Next Steps

After email is working:
1. ✅ Test email sending
2. ✅ Implement password reset
3. ⏭️ Add welcome emails (optional)
4. ⏭️ Add competition notifications (optional)

