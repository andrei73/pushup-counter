# Deployment Guide - Pushup Counter

This guide will help you deploy your pushup counter app to make it publicly accessible.

## 📋 Pre-Deployment Checklist

- [ ] Have your domain ready
- [ ] Choose a hosting platform
- [ ] Generate a new SECRET_KEY
- [ ] Decide on database (PostgreSQL recommended)
- [ ] Test locally with `DEBUG=False`

## 🚀 Recommended: Railway.app (Easiest)

### Why Railway?
- Modern, fast, and Django-friendly
- Auto-deploys from GitHub
- Built-in PostgreSQL database
- Custom domain support
- $5/month free credits

### Step-by-Step Railway Deployment

#### 1. Prepare Your Code

```bash
# Install production dependencies
pip install -r requirements_production.txt

# Create a requirements.txt for Railway (all deps)
pip freeze > requirements.txt

# Test with production settings
python manage.py collectstatic --noinput
```

#### 2. Create a GitHub Repository

```bash
cd /Users/asavoiu/Workspace/Dev_Projects/fitCounter
git init
git add .
git commit -m "Initial commit - Pushup Counter"

# Create a repo on GitHub, then:
git remote add origin https://github.com/yourusername/pushup-counter.git
git push -u origin main
```

#### 3. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your pushup-counter repository
5. Railway will auto-detect Django

#### 4. Add PostgreSQL Database

1. In your Railway project, click "New" → "Database" → "PostgreSQL"
2. Railway automatically creates and links the database
3. Environment variables are set automatically

#### 5. Configure Environment Variables

In Railway dashboard, add these variables:
```
DJANGO_SECRET_KEY=<generate-a-new-one>
ALLOWED_HOSTS=your-app.railway.app,yourdomain.com
DJANGO_SETTINGS_MODULE=pushup_counter.settings_production
```

Generate secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 6. Run Migrations

In Railway dashboard → Settings → Service → "Add Command":
```bash
python manage.py migrate
python manage.py createsuperuser --noinput  # or run manually via shell
```

#### 7. Connect Your Domain

1. In Railway: Settings → Domains → "Custom Domain"
2. Add your domain: `yourdomain.com`
3. Railway provides DNS records
4. Update your domain's DNS settings:
   - Add CNAME record pointing to Railway's domain
5. Wait for DNS propagation (up to 24 hours)

---

## 🐍 Alternative: PythonAnywhere

### Step-by-Step PythonAnywhere Deployment

#### 1. Sign Up
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Create a free account (or paid for custom domain)

#### 2. Upload Your Code

```bash
# From PythonAnywhere bash console:
git clone https://github.com/yourusername/pushup-counter.git
cd pushup-counter
```

#### 3. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 pushup-env
pip install -r requirements.txt
```

#### 4. Configure Web App

1. Go to Web tab → "Add a new web app"
2. Choose "Manual configuration" → Python 3.10
3. Set source code directory: `/home/yourusername/pushup-counter`
4. Set virtual env: `/home/yourusername/.virtualenvs/pushup-env`

#### 5. Configure WSGI File

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

path = '/home/yourusername/pushup-counter'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pushup_counter.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 6. Static Files

In Web tab → Static files section:
- URL: `/static/`
- Directory: `/home/yourusername/pushup-counter/staticfiles/`

Run in console:
```bash
python manage.py collectstatic
```

#### 7. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 8. Reload and Test

Click "Reload" button in Web tab.
Visit: `yourusername.pythonanywhere.com`

#### 9. Custom Domain (Paid Plans Only)

Web tab → Custom Domain → Add your domain
Update DNS at your registrar

---

## 🔧 Production Settings Changes

### Update settings.py

For production, modify these settings:

```python
# Generate new secret key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Disable debug
DEBUG = False

# Add your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Security Checklist

```python
# Add these to production settings:
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

## 📦 Before Going Live

### 1. Test Production Settings Locally

```bash
# Set environment variables
export DJANGO_SECRET_KEY='your-secret-key'
export DEBUG='False'
export ALLOWED_HOSTS='localhost,127.0.0.1'

# Test
python manage.py check --deploy
python manage.py runserver
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 🌐 Domain Configuration

### At Your Domain Registrar (e.g., GoDaddy, Namecheap, Google Domains)

**For Railway/Heroku:**
Add CNAME record:
- Name: `@` or `www`
- Value: `your-app.railway.app` (or provided domain)

**For PythonAnywhere:**
Add CNAME record:
- Name: `www`
- Value: `yourusername.pythonanywhere.com`

**For VPS with IP address:**
Add A record:
- Name: `@`
- Value: Your server's IP address

---

## 🔍 Common Issues & Solutions

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Connection Error
- Check environment variables
- Verify PostgreSQL is running
- Check connection string

### 500 Internal Server Error
- Check logs (Railway/PythonAnywhere dashboard)
- Verify SECRET_KEY is set
- Ensure ALLOWED_HOSTS includes your domain

### CSRF Verification Failed
- Add domain to ALLOWED_HOSTS
- Check CSRF_COOKIE_SECURE setting
- Clear browser cookies

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid | Custom Domain | PostgreSQL |
|----------|-----------|------|---------------|------------|
| **Railway** | $5 credit/month | ~$5-10/mo | ✅ Free | ✅ Included |
| **PythonAnywhere** | Yes (limited) | $5-12/mo | ✅ Paid only | ✅ MySQL free |
| **Heroku** | Eco ~$5/mo | $7-25/mo | ✅ Free | ✅ $5-9/mo |
| **DigitalOcean** | No | $5-12/mo | ✅ Free | ✅ $15/mo managed |
| **Render** | Yes (limited) | $7+/mo | ✅ Free | ✅ $7/mo |

---

## 🎯 My Recommendation

**For your use case (friends competition):**

1. **Best Overall**: Railway.app
   - Deploy in 10 minutes
   - Auto-deploys from Git
   - Built-in PostgreSQL
   - $5/month is very affordable
   - Custom domain included

2. **Best Free**: PythonAnywhere Free Tier
   - Test it out first
   - Upgrade later for custom domain
   - Good for learning

3. **Most Control**: DigitalOcean Droplet
   - If you're comfortable with servers
   - Best long-term value
   - Full control

---

## 📞 Need Help?

After choosing a platform, let me know and I can provide specific help with:
- Configuration files
- Database setup
- Domain DNS settings
- SSL certificates
- Environment variables
- Troubleshooting

Good luck with deployment! 🚀

