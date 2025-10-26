# Environment Configuration Guide

This guide explains how to configure environment variables for different deployment environments.

## 🔐 Why Environment Variables?

Environment variables allow you to:
- Keep sensitive data (like SECRET_KEY) out of version control
- Use different settings for development vs production
- Update configuration without editing code
- Avoid losing changes during `git pull`

## 📋 Available Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DJANGO_SECRET_KEY` | Django secret key for cryptographic signing | Development key | See generation below |
| `DJANGO_DEBUG` | Enable/disable debug mode | `True` | `False` (production) |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Empty (allows all in debug) | `yourusername.pythonanywhere.com` |
| `DJANGO_STATIC_ROOT` | Path where static files are collected | `BASE_DIR/staticfiles` | `/home/user/project/staticfiles` |

## 🔑 Generating a Secret Key

Run this command to generate a new secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🐍 Setting Environment Variables on PythonAnywhere

### Option 1: Using .bashrc (Recommended)

1. **Edit your .bashrc file:**
   ```bash
   nano ~/.bashrc
   ```

2. **Add these lines at the end:**
   ```bash
   # Django Environment Variables
   export DJANGO_SECRET_KEY="your-generated-secret-key-here"
   export DJANGO_DEBUG="False"
   export DJANGO_ALLOWED_HOSTS="yourusername.pythonanywhere.com"
   export DJANGO_STATIC_ROOT="/home/yourusername/pushupCounter/staticfiles"
   ```

3. **Save and reload:**
   ```bash
   source ~/.bashrc
   ```

4. **Verify:**
   ```bash
   echo $DJANGO_SECRET_KEY
   ```

### Option 2: Using WSGI Configuration File

You can also set environment variables directly in your WSGI file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import os
import sys

# Set environment variables
os.environ['DJANGO_SECRET_KEY'] = 'your-generated-secret-key-here'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['DJANGO_STATIC_ROOT'] = '/home/yourusername/pushupCounter/staticfiles'

# Add your project directory to the sys.path
path = '/home/yourusername/pushupCounter'
if path not in sys.path:
    sys.path.insert(0, path)

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'pushup_counter.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 💻 Local Development

For local development, you can:

1. **Leave environment variables unset** - The app will use sensible defaults
2. **Or create a .env file** (requires python-decouple package):
   ```bash
   pip install python-decouple
   ```
   
   Create `.env` in your project root:
   ```
   DJANGO_SECRET_KEY=your-dev-key-here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

## 🚀 Quick Setup for PythonAnywhere

Replace `yourusername` with your actual PythonAnywhere username:

```bash
# 1. Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. Edit .bashrc
nano ~/.bashrc

# 3. Add these lines (use your generated secret key):
export DJANGO_SECRET_KEY="paste-your-generated-key-here"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="yourusername.pythonanywhere.com"
export DJANGO_STATIC_ROOT="/home/yourusername/pushupCounter/staticfiles"

# 4. Save (Ctrl+X, Y, Enter) and reload
source ~/.bashrc

# 5. Activate your virtualenv
workon pushupenv

# 6. Run collectstatic
cd ~/pushupCounter
python manage.py collectstatic --noinput

# 7. Reload your web app
# Go to PythonAnywhere Web tab and click "Reload"
```

## ✅ Verification

After setting up, verify your configuration:

```python
# In Django shell
python manage.py shell

>>> from django.conf import settings
>>> print(f"DEBUG: {settings.DEBUG}")
>>> print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
>>> print(f"SECRET_KEY: {settings.SECRET_KEY[:10]}...")  # Only show first 10 chars
>>> print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
```

## 🔄 After Git Pull

The beauty of this setup is that after a `git pull`, you don't need to edit `settings.py` anymore! Your environment variables will persist, and the code will automatically use them.

Just run:
```bash
cd ~/pushupCounter
git pull origin develop
python manage.py migrate  # If there are database changes
python manage.py collectstatic --noinput
# Reload web app from PythonAnywhere Web tab
```

## 🛡️ Security Best Practices

1. ✅ **DO**: Keep your secret key secret (never commit it)
2. ✅ **DO**: Set `DEBUG=False` in production
3. ✅ **DO**: Use a strong, randomly generated secret key
4. ✅ **DO**: Specify exact hostnames in `ALLOWED_HOSTS`
5. ❌ **DON'T**: Commit `.env` files or expose secrets in version control
6. ❌ **DON'T**: Use the same secret key in development and production

## 📝 Example Values

### Development (Local):
```bash
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
# SECRET_KEY and STATIC_ROOT can use defaults
```

### Production (PythonAnywhere):
```bash
DJANGO_SECRET_KEY="django-insecure-abc123xyz789..."
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=asavoiu.pythonanywhere.com
DJANGO_STATIC_ROOT=/home/asavoiu/pushupCounter/staticfiles
```

## 🆘 Troubleshooting

**Problem**: Changes not taking effect
- **Solution**: Make sure to reload the web app from PythonAnywhere Web tab after changing environment variables

**Problem**: `ALLOWED_HOSTS` not working
- **Solution**: Check for extra spaces or quotes. Use: `export DJANGO_ALLOWED_HOSTS="host1.com,host2.com"` (no spaces after commas)

**Problem**: Static files not loading
- **Solution**: Verify `DJANGO_STATIC_ROOT` is set correctly and run `collectstatic` again

**Problem**: Environment variables not persisting
- **Solution**: Make sure you added them to `~/.bashrc` and ran `source ~/.bashrc`

