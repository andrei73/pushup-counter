# 🏆 Monthly Competition Feature

## Overview

The Monthly Competition feature adds a formal structure to your pushup challenges, with automatic winner declaration, competition history, and winner badges.

## Key Features

### 1. **Structured Monthly Competitions**
- Each month is a formal competition with clear start/end dates
- Automatic status tracking (Upcoming → Active → Completed)
- Winner determination at month end

### 2. **Winner Recognition System**
- 🏆 Winner badges displayed on profiles and leaderboard
- "Nx Champion" badges showing total wins
- Last month's winner banner on dashboard
- Competition archive with historical winners

### 3. **Competition Dashboard**
- **Current Competition Banner**: Shows active competition with countdown
- **Last Month's Winner**: Celebrates previous winner
- **Days Remaining**: Live countdown to competition end
- **Your Position**: Real-time rank in current competition

### 4. **Competition Archive**
- View all past, current, and upcoming competitions
- Detailed competition pages with full leaderboards
- Winner history and statistics

### 5. **Activity Feed Integration**
- Competition context for all pushup entries
- Visual competition status indicators

## What's New on Each Page

### Dashboard
- **Competition Banner**: Purple gradient card showing current competition
- **Winner Announcement**: Gold banner celebrating last month's champion
- **Position Badge**: Your current rank in the competition

### Leaderboard
- **Winner Badges**: Gold "Nx Champion" badges next to usernames
- Shows how many times each user has won

### User Profiles
- **Large Winner Badge**: Prominently displays championship count
- "Nx Champion" title under username

### New Pages
- **Competitions** (`/competitions/`): Archive of all competitions
- **Competition Detail** (`/competitions/<id>/`): Full details and leaderboard for specific competition

## Database Schema

### Competition Model
```python
- name: "October 2025" (auto-generated)
- start_date: First day of month
- end_date: Last day of month
- status: upcoming/active/completed
- winner: User who won (auto-determined)
- winner_total: Winner's pushup count
```

## Management Commands

### Create Competitions
```bash
# Create competition for current month
python manage.py create_competitions

# Create competition for specific month
python manage.py create_competitions --year 2025 --month 11

# Create next 3 months
python manage.py create_competitions --months 3

# Update status of all competitions
python manage.py create_competitions --update-status
```

### Admin Actions
From Django admin, you can:
- Manually create/edit competitions
- Update competition status
- Force determine winners
- View all competition data

## How It Works

### 1. Competition Lifecycle

**Upcoming** (before start date):
- Status: "Upcoming"
- Not yet accepting entries (but entries are tracked by date)
- Displayed in "Upcoming" section of archive

**Active** (between start and end date):
- Status: "Active"
- Banner displayed on dashboard
- Countdown timer shows days remaining
- Real-time leaderboard updates

**Completed** (after end date):
- Status: "Completed"
- Winner automatically determined
- Winner badge awarded
- Moved to "Past Competitions" archive

### 2. Winner Determination

Winner is automatically determined when:
- Competition end date passes
- `update_status()` is called (happens on page views)
- Admin manually triggers "Determine winners" action

Winner is the user with highest total pushups for that month.

### 3. Badge System

Winner badges show:
- **1x Champion**: Won once
- **2x Champion**: Won twice
- **3x Champion**: Won three times, etc.

Badges appear:
- Next to username in leaderboard
- On user profile (large badge)
- In competition detail pages

## Testing Steps

### Initial Setup

1. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Install New Dependency**
   ```bash
   pip install python-dateutil==2.9.0
   ```

3. **Create October 2025 Competition**
   ```bash
   python manage.py create_competitions --year 2025 --month 10
   ```

4. **Create Past Competitions** (for testing winner badges)
   ```bash
   python manage.py create_competitions --year 2025 --month 9
   python manage.py create_competitions --year 2025 --month 8
   ```

5. **Manually Set Winners** (via Django admin)
   - Go to `/admin/tracker/competition/`
   - Edit September and August competitions
   - Set status to "Completed"
   - Choose a winner and set winner_total
   - Save

### What to Test

#### ✅ Dashboard
- [ ] See purple competition banner for October 2025
- [ ] Countdown shows correct days remaining
- [ ] Your position is displayed
- [ ] "View All Competitions" button works
- [ ] Gold winner banner shows September winner (if set)
- [ ] "You won!" badge appears if you were winner

#### ✅ Leaderboard
- [ ] Winner badges (🏆 Nx) appear next to past winners
- [ ] Badges show correct win count
- [ ] Hover shows "N times champion" tooltip

#### ✅ User Profiles
- [ ] Large "Nx Champion" badge appears for winners
- [ ] Badge shows correct count
- [ ] Badge only shows if user has wins

#### ✅ Competitions Page (`/competitions/`)
- [ ] Current competition shows in "Active Now" section
- [ ] Past competitions show in "Past Competitions"
- [ ] Winner info displayed on completed competitions
- [ ] "View Leaderboard" and "View Details" buttons work

#### ✅ Competition Detail Page
- [ ] Shows competition status and info
- [ ] Displays participant count
- [ ] Shows days remaining (if active)
- [ ] Winner banner appears (if completed)
- [ ] Full leaderboard displayed
- [ ] Winner badges show on leaderboard

#### ✅ Admin Interface
- [ ] Competition model appears in admin
- [ ] Can create new competitions
- [ ] Can update status (bulk action)
- [ ] Can determine winners (bulk action)
- [ ] Fieldsets properly organized

## Automation (Future)

You can automate competition creation using:

### Cron Job (PythonAnywhere)
```bash
# Add to crontab (runs on 1st of each month at midnight)
0 0 1 * * cd /home/yourusername/pushupCounter && /home/yourusername/.virtualenvs/pushupenv/bin/python manage.py create_competitions
```

### Django-cron or Celery Beat
For more robust scheduling, consider:
- `django-cron`: Simple periodic tasks
- `Celery Beat`: Advanced task scheduling

## UI Customization

All competition styling is in `base.html`:
- `.winner-badge`: Small badges on leaderboard
- `.winner-badge-large`: Large badges on profiles
- `.competition-status-badge`: Status indicators (Active/Completed/Upcoming)
- Competition banners use gradient colors:
  - Purple: Active competition
  - Gold: Winner announcements
  - Blue: Upcoming
  - Gray: Completed

## Technical Notes

### Performance Optimization
Winner badges are calculated per-request. For high-traffic sites, consider:
- Caching win counts
- Denormalizing win count to User model
- Using select_related/prefetch_related

### Winner Determination Logic
```python
def determine_winner(self):
    """Get user with highest total pushups in competition month"""
    entries = PushupEntry.objects.filter(
        date__year=self.year,
        date__month=self.month
    ).values('user').annotate(
        total=Sum('count')
    ).order_by('-total').first()
```

### Status Update Logic
Status is automatically updated when:
- `Competition.get_current_competition()` is called
- Page loads that fetch competition data
- Admin actions run

You can manually trigger with:
```bash
python manage.py create_competitions --update-status
```

## Troubleshooting

### No competitions showing?
- Run `python manage.py create_competitions`
- Check admin for existing competitions

### Winner not determined?
- Ensure competition end date has passed
- Run `update-status` command
- Use admin "Determine winners" action

### Wrong winner?
- Check pushup entries for that month
- Verify date range matches competition
- Manually correct in admin if needed

### Badges not showing?
- Ensure competition status is "Completed"
- Verify winner is set on competition
- Clear browser cache

## Future Enhancements

Potential additions:
- **Weekly competitions**: Shorter competitive periods
- **Team competitions**: Group-based challenges
- **Special events**: Holiday challenges, marathons
- **Email notifications**: Winner announcements
- **Winner streaks**: Track consecutive wins
- **Achievements**: Unlock badges for milestones
- **Leaderboard filtering**: View specific competitions
- **Statistics dashboard**: Competition analytics

---

🎉 **Congratulations!** You now have a full-featured competition system with winner recognition, archives, and automated tracking!

