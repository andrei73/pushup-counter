# 🚀 PythonAnywhere Quick Setup

This is a **quick reference** for deploying updates to PythonAnywhere. For detailed information, see [ENV_CONFIG.md](ENV_CONFIG.md).

## 🔧 One-Time Setup (After First Deployment)

Only do this **once** after your initial deployment:

### Step 1: Generate a Secret Key

```bash
cd ~/pushupCounter
workon pushupenv
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key!

### Step 2: Set Environment Variables

```bash
nano ~/.bashrc
```

Add these lines at the end (replace `yourusername` and paste your generated secret key):

```bash
# Django Environment Variables
export DJANGO_SECRET_KEY="paste-your-generated-secret-key-here"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="yourusername.pythonanywhere.com"
export DJANGO_STATIC_ROOT="/home/yourusername/pushupCounter/staticfiles"
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 3: Reload Environment

```bash
source ~/.bashrc
```

### Step 4: Verify

```bash
echo $DJANGO_SECRET_KEY
echo $DJANGO_ALLOWED_HOSTS
```

You should see your secret key and hostname!

---

## 🔄 Regular Deployment (Every Time You Update Code)

After you've done the one-time setup above, follow these steps **every time** you push new code:

### 1. SSH into PythonAnywhere
Log in to your PythonAnywhere console.

### 2. Pull Latest Changes

```bash
cd ~/pushupCounter
workon pushupenv
git checkout develop
git pull origin develop
```

### 3. Run Migrations (if any database changes)

```bash
python manage.py migrate
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Reload Web App

Go to the **Web** tab in PythonAnywhere dashboard and click the big green **"Reload"** button.

---

## ✅ That's It!

Your environment variables will persist across deployments. No more losing `ALLOWED_HOSTS` or `STATIC_ROOT` settings! 🎉

---

## 🆘 Troubleshooting

### Problem: `ALLOWED_HOSTS` error
**Solution**: Make sure you set the environment variable correctly in `~/.bashrc` and ran `source ~/.bashrc`.

### Problem: Static files not loading
**Solution**: Check that `DJANGO_STATIC_ROOT` is set and run `collectstatic` again.

### Problem: Environment variables not working
**Solution**: 
```bash
# Check if they're set
echo $DJANGO_DEBUG
echo $DJANGO_ALLOWED_HOSTS

# If empty, reload .bashrc
source ~/.bashrc
```

### Problem: Still getting errors
**Solution**: Check your WSGI configuration at `/var/www/yourusername_pythonanywhere_com_wsgi.py` and make sure it's loading your virtualenv correctly.

---

## 📚 For More Details

- Full environment configuration guide: [ENV_CONFIG.md](ENV_CONFIG.md)
- Deployment guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- PWA setup: [PWA_SETUP_AND_TESTING.md](PWA_SETUP_AND_TESTING.md)

