# Pushup Counter Web App 💪

A Django-based web application for tracking pushup competitions among friends. Perfect for monthly fitness challenges!

## Features

- 🏋️ **Track Daily Pushups**: Log your pushup count every day with optional notes
- 🏆 **Real-time Leaderboard**: See how you rank against your friends in monthly competitions
- 📊 **Personal Statistics**: Track your total, average, best day, and active days
- 👥 **Public Registration**: Anyone can create an account and join the competition
- 🔒 **Fair Play**: Regular users can only add today's pushups (prevents backdating)
- 👑 **Admin Privileges**: Admins can add historical data for any date
- 📱 **Responsive Design**: Beautiful, modern UI built with Bootstrap 5
- 📈 **Charts & Visualizations**: Visual progress tracking (Chart.js ready)

## Technology Stack

- **Backend**: Django 5.1.4
- **Frontend**: Bootstrap 5.3.2, Bootstrap Icons
- **Database**: SQLite (development) - easily upgradable to PostgreSQL
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Charts**: Chart.js (integrated)

## Project Structure

```
fitCounter/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── db.sqlite3                   # Database (created after migrations)
├── pushup_counter/              # Main project settings
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI application
│   └── asgi.py                  # ASGI application
├── tracker/                     # Main application
│   ├── __init__.py
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── forms.py                 # Form definitions
│   ├── urls.py                  # App URL patterns
│   ├── admin.py                 # Admin configuration
│   ├── apps.py                  # App configuration
│   ├── migrations/              # Database migrations
│   └── templates/tracker/       # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── dashboard.html
│       ├── leaderboard.html
│       ├── entry_form.html
│       ├── entry_confirm_delete.html
│       ├── history.html
│       ├── profile.html
│       ├── login.html
│       └── signup.html
├── static/                      # Static files (CSS, JS)
│   ├── css/
│   └── js/
└── venv/                        # Virtual environment

```

## Quick Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (already created in your case)

### Installation Steps

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - **Main app**: http://127.0.0.1:8000/
   - **Admin panel**: http://127.0.0.1:8000/admin/

## Usage Guide

### For Regular Users

1. **Sign Up**: Create an account from the homepage
2. **Add Pushups**: Click "Add Pushups" in the navigation
3. **Today Only**: You can only log pushups for today's date
4. **Multiple Entries**: You can add multiple entries per day (they'll be summed)
5. **View Progress**: Check your dashboard for stats and rankings
6. **Leaderboard**: See how you compare to your friends
7. **History**: View all your past entries with filtering options

### For Admin Users

1. **Login**: Use your superuser credentials
2. **Admin Panel**: Access at `/admin/` for full database control
3. **Any Date**: Admins can add entries for any date (historical data import)
4. **User Management**: Manage all users and their entries
5. **Bulk Operations**: Perform bulk updates via admin interface

### Contest Rules

- ✅ Regular users can only log pushups for **today's date**
- ✅ Multiple entries per day are **allowed** (e.g., 50 in morning, 30 in evening)
- ✅ Rankings are calculated based on the **current month's total**
- ✅ Each user can edit/delete their own entries
- ✅ Admins can add historical data if needed
- ❌ No backdating for regular users (keeps competition fair!)

## Key Features Explained

### Dashboard
- **Total Pushups**: Your sum for the current month
- **Daily Average**: Total divided by active days
- **Best Day**: Your highest single-day total
- **Your Rank**: Current position in the leaderboard
- **Recent Activity**: Last 10 entries with edit/delete options

### Leaderboard
- **Monthly Rankings**: All users sorted by total pushups
- **Trophy Icons**: Gold, silver, bronze for top 3
- **Highlight**: Your position is highlighted
- **Competition Stats**: Total competitors and leader's score

### Entry Management
- **Date Validation**: Automatic enforcement of date restrictions
- **Form Validation**: Ensures positive pushup counts
- **Edit/Delete**: Full control over your entries
- **Notes Field**: Add optional notes to each entry

### Profile
- **User Stats**: Personal statistics and rankings
- **Recent Activity**: Your last 10 entries
- **Public Profiles**: View other users' profiles (without edit access)

## Advanced Configuration

### Changing the Secret Key (Production)
Edit `pushup_counter/settings.py`:
```python
SECRET_KEY = 'your-new-secret-key-here'
```

### Using PostgreSQL (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pushup_counter_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Allowed Hosts (Production)
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### Static Files (Production)
```bash
python manage.py collectstatic
```

## Troubleshooting

### Issue: Can't install crispy-bootstrap5
**Solution**: Make sure you have the correct version (2025.6)
```bash
pip install crispy-bootstrap5==2025.6
```

### Issue: Migration errors
**Solution**: Delete migrations and recreate
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

### Issue: Date validation not working
**Solution**: Make sure you're logged in and check if you're an admin

### Issue: Static files not loading
**Solution**: Run collectstatic or ensure DEBUG=True in development

## Development Tips

### Creating Test Data
Use the Django shell to create test entries:
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from tracker.models import PushupEntry
from django.utils import timezone

user = User.objects.get(username='your_username')
PushupEntry.objects.create(user=user, date=timezone.now().date(), count=50)
```

### Running Tests
```bash
python manage.py test
```

### Database Shell
```bash
python manage.py dbshell
```

## Future Enhancements

- [ ] Add data export (CSV/PDF)
- [ ] Email notifications for leaderboard changes
- [ ] Weekly/yearly views
- [ ] Goals and achievements system
- [ ] Social sharing features
- [ ] Mobile app (React Native/Flutter)
- [ ] API endpoints (Django REST Framework)
- [ ] Multiple contest types (teams, weight categories)

## Contributing

Feel free to fork this project and add your own features!

## License

This project is open source and available for personal use.

## Support

If you encounter any issues or have questions, please check the troubleshooting section or create an issue.

---

**Built with ❤️ using Django 5 & Bootstrap 5**

Enjoy your pushup contest! 💪 Keep pushing!


