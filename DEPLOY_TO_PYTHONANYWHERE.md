# 🚀 Deploy to PythonAnywhere - Complete Guide

## 📦 What's Being Deployed

### Commit 1: UX Improvements (4b05b0a)
- ✅ Floating Action Button (FAB) for mobile
- ✅ History page total pushups display
- ✅ Dashboard lifetime total stat
- ✅ Timezone fix (local date vs UTC)

### Commit 2: Competition Admin Fix (0fc607f)
- ✅ Auto-determine winner when status changes to completed
- ✅ Enhanced admin actions with better feedback

---

## 🔧 Step-by-Step Deployment

### Step 1: Push to GitHub (Local Machine)

```bash
cd /Users/asavoiu/Workspace/Dev_Projects/fitCounter

# Push all commits to develop branch
git push origin develop
```

**If you get certificate errors**, use SSH instead:
```bash
git remote set-url origin git@github.com:andrei73/pushup-counter.git
git push origin develop
```

---

### Step 2: Connect to PythonAnywhere

Open your terminal and SSH into PythonAnywhere:

```bash
ssh asavoiu@ssh.pythonanywhere.com
```

Or use the PythonAnywhere web console (easier):
1. Go to https://www.pythonanywhere.com
2. Click "Consoles" tab
3. Start a new "Bash" console

---

### Step 3: Navigate and Pull Changes

```bash
# Navigate to project directory
cd ~/pushupCounter

# Activate virtual environment
workon pushupenv

# Pull latest changes from develop branch
git pull origin develop
```

**Expected Output:**
```
remote: Enumerating objects...
remote: Counting objects: 100% (X/X), done.
Updating 4b05b0a..0fc607f
Fast-forward
 tracker/admin.py                    | 28 ++++++++++++++++++-
 tracker/templates/tracker/base.html | 52 ++++++++++++++++++++++++++++++++++
 tracker/templates/tracker/dashboard.html | 11 +++++--
 tracker/templates/tracker/history.html | 18 ++++++++++--
 tracker/views.py                    | 23 +++++++++------
 tracker/forms.py                    | 8 +++---
 UX_IMPROVEMENTS_MOBILE.md          | 599 ++++++++++++++++++++++++++++++++++++++
 TIMEZONE_FIX.md                    | 298 +++++++++++++++++++
 COMPETITION_ADMIN_FIX.md           | 407 +++++++++++++++++++++++++
 9 files changed, 1104 insertions(+), 11 deletions(-)
```

---

### Step 4: Fix October Competition Winner (Quick Fix)

Since you already changed October to "completed" but it doesn't have a winner, let's fix that now:

```bash
# Still in ~/pushupCounter with pushupenv activated
python manage.py shell
```

Then in the Python shell:
```python
from tracker.models import Competition

# Get October 2025 competition
oct_comp = Competition.objects.get(name="October 2025")

# Check current status
print(f"Status: {oct_comp.status}")
print(f"Winner: {oct_comp.winner}")
print(f"Winner Total: {oct_comp.winner_total}")

# Determine the winner
oct_comp.determine_winner()

# Verify it worked
print(f"\n✅ After determining winner:")
print(f"Winner: {oct_comp.winner}")
print(f"Winner Total: {oct_comp.winner_total}")

# Exit shell
exit()
```

**Expected Output:**
```
Status: completed
Winner: None
Winner Total: None

✅ After determining winner:
Winner: username_here
Winner Total: 1234
```

---

### Step 5: Collect Static Files

The CSS changes for the FAB button need to be collected:

```bash
python manage.py collectstatic --noinput
```

**Expected Output:**
```
X static files copied to '/home/asavoiu/pushupCounter/staticfiles'.
```

---

### Step 6: Reload Web App

**Option A: Web Interface (Recommended)**
1. Go to https://www.pythonanywhere.com
2. Click "Web" tab
3. Click the green **"Reload asavoiu.pythonanywhere.com"** button
4. Wait for "✅ Reload successful" message

**Option B: Command Line**
```bash
touch /var/www/asavoiu_pythonanywhere_com_wsgi.py
```

---

## 🧪 Testing After Deployment

### Test 1: Desktop View (On Your Laptop)

Visit: `https://asavoiu.pythonanywhere.com/dashboard/`

**Check:**
- [ ] New "Lifetime Total" stat card visible (6th card, purple)
- [ ] Quick Actions section visible below stats
- [ ] FAB button NOT visible
- [ ] "Last Month's Champion" banner shows October winner
- [ ] All stat cards show correct numbers

Visit: `https://asavoiu.pythonanywhere.com/history/`

**Check:**
- [ ] Total badge in top-right corner
- [ ] Filter by year/month updates total
- [ ] Footer shows entry count and total pushups

---

### Test 2: Mobile View (Chrome DevTools)

On your laptop:
1. Visit https://asavoiu.pythonanywhere.com
2. Press F12 (open DevTools)
3. Press Ctrl+Shift+M (Cmd+Shift+M on Mac) - Toggle Device Toolbar
4. Select "iPhone 12 Pro" or "Pixel 5"

Visit dashboard:

**Check:**
- [ ] FAB button visible in bottom-right corner
- [ ] FAB button has purple gradient
- [ ] FAB button stays visible when scrolling
- [ ] Quick Actions section is HIDDEN
- [ ] Tap FAB → goes to Add Pushups page
- [ ] "Lifetime Total" card visible
- [ ] "Last Month's Champion" banner visible

---

### Test 3: PWA on Phone

On your actual phone:
1. Open the installed PWA app
2. Go to Dashboard

**Check:**
- [ ] FAB button visible and accessible
- [ ] FAB doesn't overlap other content
- [ ] Can tap FAB to add pushups
- [ ] October winner banner shows
- [ ] All stats display correctly

---

### Test 4: Admin Interface

Visit: `https://asavoiu.pythonanywhere.com/admin/`

**Test Auto-Determination:**
1. Go to Competitions
2. Create a test competition or use existing
3. Change status to "completed"
4. Click "Save"
5. **Check:** Success message shows winner details
6. **Check:** Winner and winner_total fields populated

**Test Admin Action:**
1. Go to Competitions
2. Select October 2025 competition
3. Actions → "Determine winners for completed competitions"
4. Click "Go"
5. **Check:** Success message with winner info

---

## 🐛 Troubleshooting

### Issue 1: FAB Button Not Visible on Mobile

**Symptoms:** No floating button on mobile view

**Fix:**
```bash
cd ~/pushupCounter
workon pushupenv
python manage.py collectstatic --noinput
# Then reload web app
```

**Verify:** Check that CSS file was collected:
```bash
ls staticfiles/  # Should show updated files
```

---

### Issue 2: October Winner Still Not Showing

**Symptoms:** Banner doesn't appear on dashboard

**Fix Option A - Admin Action:**
1. Go to Admin → Competitions
2. Select October 2025
3. Actions → "Determine winners"
4. Click "Go"

**Fix Option B - Shell:**
```bash
python manage.py shell
```
```python
from tracker.models import Competition
comp = Competition.objects.get(name="October 2025")
comp.determine_winner()
print(f"Winner: {comp.winner}, Total: {comp.winner_total}")
exit()
```

**Fix Option C - Management Command:**
```bash
python manage.py create_competitions --update-status
```

---

### Issue 3: Static Files Not Loading

**Symptoms:** FAB button missing, styles broken

**Fix:**
```bash
cd ~/pushupCounter
workon pushupenv

# Check static root setting
python manage.py shell -c "from django.conf import settings; print(settings.STATIC_ROOT)"

# Should output: /home/asavoiu/pushupCounter/staticfiles

# Re-collect static files
python manage.py collectstatic --noinput

# Verify permissions
ls -la staticfiles/

# Reload web app
```

---

### Issue 4: Git Pull Fails

**Symptoms:** `error: Your local changes would be overwritten by merge`

**Fix:**
```bash
cd ~/pushupCounter

# Check what's different
git status

# Stash local changes
git stash

# Pull again
git pull origin develop

# If needed, reapply stash
git stash pop
```

---

### Issue 5: Changes Not Visible After Reload

**Symptoms:** Still seeing old version

**Fix:**
```bash
# Hard reload in PythonAnywhere

# 1. Stop any running processes
ps aux | grep python

# 2. Force reload WSGI
touch /var/www/asavoiu_pythonanywhere_com_wsgi.py

# 3. Clear browser cache
# In browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)

# 4. Check error log
tail -50 /var/log/asavoiu.pythonanywhere.com.error.log
```

---

## 📊 Verification Checklist

### Before Deployment
- [x] Local testing completed
- [x] All commits on develop branch
- [ ] Git push successful
- [ ] GitHub shows latest commits

### After Deployment
- [ ] Git pull successful on PythonAnywhere
- [ ] October competition winner determined
- [ ] Static files collected
- [ ] Web app reloaded
- [ ] Desktop view tested
- [ ] Mobile view tested (DevTools)
- [ ] PWA tested on phone
- [ ] Admin interface tested

---

## 📱 Feature Summary

### What Your Friends Will See

**Mobile Users (PWA):**
- 🎯 Floating "+ " button always accessible (no scrolling!)
- 📊 See lifetime total pushups (not just monthly)
- 🔢 History page shows total for filtered results
- 🏆 October winner banner on dashboard
- ✅ Correct "today" date (timezone fixed)

**Desktop Users:**
- 📊 New "Lifetime Total" stat on dashboard
- 🔢 History totals in header and footer
- 🏆 October winner banner
- 🎨 Quick Actions section visible

**Admin Users:**
- ⚡ Automatic winner determination
- 📝 Detailed feedback messages
- 🔧 Enhanced admin actions

---

## 🔄 Rollback Plan (If Needed)

If something goes wrong and you need to rollback:

```bash
cd ~/pushupCounter
workon pushupenv

# Find previous commit hash
git log --oneline -5

# Rollback to before these changes
git checkout <previous-commit-hash>

# Force static files to old version
python manage.py collectstatic --noinput

# Reload web app
```

**Then in PythonAnywhere Web tab:** Click "Reload"

**To return to latest:**
```bash
git checkout develop
git pull origin develop
python manage.py collectstatic --noinput
# Reload web app
```

---

## 📞 Support Resources

### Error Logs
```bash
# View recent errors
tail -100 /var/log/asavoiu.pythonanywhere.com.error.log

# Follow logs in real-time
tail -f /var/log/asavoiu.pythonanywhere.com.error.log
```

### Django Shell (Debug)
```bash
python manage.py shell
```
```python
# Check competition status
from tracker.models import Competition
for c in Competition.objects.all():
    print(f"{c.name}: {c.status}, Winner: {c.winner}")

# Check user stats
from tracker.models import PushupEntry
from django.contrib.auth.models import User
user = User.objects.get(username='your_username')
total = PushupEntry.objects.filter(user=user).aggregate(Sum('count'))
print(f"Lifetime total: {total}")
```

### PythonAnywhere Forum
- https://www.pythonanywhere.com/forums/

### Documentation Links
- UX_IMPROVEMENTS_MOBILE.md - Detailed feature documentation
- TIMEZONE_FIX.md - Timezone issue explanation
- COMPETITION_ADMIN_FIX.md - Admin fix details

---

## ✨ Summary

### Files Changed
- `tracker/views.py` - Lifetime total, history total, timezone fixes
- `tracker/forms.py` - Timezone fix for date validation
- `tracker/templates/tracker/base.html` - FAB CSS and HTML
- `tracker/templates/tracker/dashboard.html` - Lifetime stat, responsive classes
- `tracker/templates/tracker/history.html` - Total displays
- `tracker/admin.py` - Auto winner determination

### Database Changes
- ✅ **None!** No migrations needed

### Static Files
- ✅ CSS updates (FAB styles)
- ✅ Requires `collectstatic`

### Deployment Time
- ⏱️ ~5 minutes total
- Most time: git pull + static files

---

## 🎉 Success Criteria

Deployment is successful when:
- ✅ FAB button visible on mobile
- ✅ Lifetime total shows on dashboard
- ✅ History shows filtered totals
- ✅ October winner banner visible
- ✅ Timezone shows correct day
- ✅ Admin auto-determines winners
- ✅ No error messages in logs
- ✅ Friends can test on their phones

**You're all set! Deploy with confidence!** 💪🚀

