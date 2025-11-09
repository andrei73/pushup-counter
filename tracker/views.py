from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from .models import PushupEntry, Competition
from .forms import SignUpForm, PushupEntryForm


def home(request):
    """Home page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')


def signup(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'tracker/signup.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard with personal stats."""
    from datetime import date
    today = date.today()  # Use local server date instead of UTC
    current_year = today.year
    current_month = today.month
    
    # Get user's monthly stats
    stats = PushupEntry.get_user_stats(request.user, current_year, current_month)
    
    # Get today's pushup count
    today_total = PushupEntry.objects.filter(
        user=request.user,
        date=today
    ).aggregate(total=Sum('count'))['total'] or 0
    
    # Get lifetime total (all time)
    lifetime_total = PushupEntry.objects.filter(
        user=request.user
    ).aggregate(total=Sum('count'))['total'] or 0
    
    # Get daily pushup data for chart
    from calendar import monthrange
    from datetime import date
    
    # Get number of days in current month
    days_in_month = monthrange(current_year, current_month)[1]
    
    # Get all entries for current month grouped by day
    daily_data = PushupEntry.objects.filter(
        user=request.user,
        date__year=current_year,
        date__month=current_month
    ).values('date').annotate(total=Sum('count')).order_by('date')
    
    # Create a dictionary for easy lookup
    daily_dict = {entry['date'].day: entry['total'] for entry in daily_data}
    
    # Create lists for chart (all days of month)
    chart_labels = list(range(1, days_in_month + 1))
    chart_data = [daily_dict.get(day, 0) for day in chart_labels]
    
    # Get user's recent entries
    recent_entries = PushupEntry.objects.filter(user=request.user)[:10]
    
    # Get user's rank in current month
    leaderboard = PushupEntry.get_monthly_leaderboard(current_year, current_month)
    user_rank = None
    for idx, entry in enumerate(leaderboard, 1):
        if entry['user__id'] == request.user.id:
            user_rank = idx
            break
    
    # Get recent activity feed (all users)
    activity_feed = PushupEntry.objects.select_related('user').order_by('-created_at')[:15]
    
    # Calculate yesterday for activity feed
    from datetime import timedelta
    yesterday = today - timedelta(days=1)
    
    # Get current competition
    current_competition = Competition.get_current_competition()
    
    # Get last completed competition (for winner announcement)
    last_competition = Competition.get_last_completed_competition()
    
    # Get user's win count (for badges)
    win_count = Competition.objects.filter(winner=request.user, status=Competition.COMPLETED).count()
    
    context = {
        'stats': stats,
        'today_total': today_total,
        'lifetime_total': lifetime_total,
        'recent_entries': recent_entries,
        'user_rank': user_rank,
        'total_competitors': leaderboard.count(),
        'current_month': today.strftime('%B %Y'),
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'activity_feed': activity_feed,
        'today': today,
        'yesterday': yesterday,
        'current_competition': current_competition,
        'last_competition': last_competition,
        'win_count': win_count,
    }
    
    return render(request, 'tracker/dashboard.html', context)


@login_required
def leaderboard(request):
    """Leaderboard view showing all users' rankings."""
    from datetime import date
    today = date.today()
    current_year = today.year
    current_month = today.month
    
    # Get monthly leaderboard
    leaderboard_data = PushupEntry.get_monthly_leaderboard(current_year, current_month)
    
    # Add win count to each leaderboard entry
    from django.contrib.auth.models import User
    leaderboard_with_wins = []
    for entry in leaderboard_data:
        user = User.objects.get(id=entry['user__id'])
        win_count = Competition.objects.filter(winner=user, status=Competition.COMPLETED).count()
        entry_dict = dict(entry)
        entry_dict['win_count'] = win_count
        leaderboard_with_wins.append(entry_dict)
    
    # Get current competition
    current_competition = Competition.get_current_competition()
    
    context = {
        'leaderboard': leaderboard_with_wins,
        'current_month': today.strftime('%B %Y'),
        'current_user_id': request.user.id,
        'current_competition': current_competition,
    }
    
    return render(request, 'tracker/leaderboard.html', context)


@login_required
def add_entry(request):
    """Add a new pushup entry."""
    if request.method == 'POST':
        form = PushupEntryForm(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f'Added {entry.count} pushups for {entry.date}!')
            return redirect('dashboard')
    else:
        form = PushupEntryForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Add Pushups',
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'tracker/entry_form.html', context)


@login_required
def edit_entry(request, pk):
    """Edit an existing pushup entry."""
    entry = get_object_or_404(PushupEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PushupEntryForm(request.POST, instance=entry, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect('dashboard')
    else:
        form = PushupEntryForm(instance=entry, user=request.user)
    
    context = {
        'form': form,
        'title': 'Edit Entry',
        'entry': entry,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'tracker/entry_form.html', context)


@login_required
def delete_entry(request, pk):
    """Delete a pushup entry."""
    entry = get_object_or_404(PushupEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect('dashboard')
    
    context = {'entry': entry}
    return render(request, 'tracker/entry_confirm_delete.html', context)


@login_required
def history(request):
    """View all entries with filtering options."""
    from django.db.models import Sum
    
    entries = PushupEntry.objects.filter(user=request.user)
    
    # Get filter parameters
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year:
        entries = entries.filter(date__year=year)
    if month:
        entries = entries.filter(date__month=month)
    
    # Calculate total pushups for filtered entries
    total_pushups = entries.aggregate(total=Sum('count'))['total'] or 0
    
    # Get available years for filter dropdown
    years = PushupEntry.objects.filter(user=request.user).dates('date', 'year', order='DESC')
    
    context = {
        'entries': entries,
        'years': years,
        'selected_year': year,
        'selected_month': month,
        'total_pushups': total_pushups,
    }
    
    return render(request, 'tracker/history.html', context)


@login_required
def profile(request, username=None):
    """View a user's profile and stats."""
    from django.contrib.auth.models import User
    from calendar import monthrange
    
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    from datetime import date
    today = date.today()
    current_year = today.year
    current_month = today.month
    
    # Get user's stats
    stats = PushupEntry.get_user_stats(profile_user, current_year, current_month)
    
    # Get daily pushup data for chart
    days_in_month = monthrange(current_year, current_month)[1]
    
    # Get all entries for current month grouped by day
    daily_data = PushupEntry.objects.filter(
        user=profile_user,
        date__year=current_year,
        date__month=current_month
    ).values('date').annotate(total=Sum('count')).order_by('date')
    
    # Create a dictionary for easy lookup
    daily_dict = {entry['date'].day: entry['total'] for entry in daily_data}
    
    # Create lists for chart (all days of month)
    chart_labels = list(range(1, days_in_month + 1))
    chart_data = [daily_dict.get(day, 0) for day in chart_labels]
    
    # Get user's rank
    leaderboard = PushupEntry.get_monthly_leaderboard(current_year, current_month)
    user_rank = None
    total_users = leaderboard.count()
    for idx, entry in enumerate(leaderboard, 1):
        if entry['user__id'] == profile_user.id:
            user_rank = idx
            break
    
    # Get recent entries
    recent_entries = PushupEntry.objects.filter(user=profile_user)[:10]
    
    # Calculate comparison with current user (if viewing someone else's profile)
    comparison = None
    if profile_user != request.user:
        current_user_stats = PushupEntry.get_user_stats(request.user, current_year, current_month)
        difference = stats['total'] - current_user_stats['total']
        comparison = {
            'difference': abs(difference),
            'ahead': difference > 0,
            'behind': difference < 0,
            'tied': difference == 0
        }
    
    # Get user's win count (for badges)
    win_count = Competition.objects.filter(winner=profile_user, status=Competition.COMPLETED).count()
    
    context = {
        'profile_user': profile_user,
        'stats': stats,
        'user_rank': user_rank,
        'total_users': total_users,
        'recent_entries': recent_entries,
        'current_month': today.strftime('%B %Y'),
        'is_own_profile': profile_user == request.user,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'comparison': comparison,
        'win_count': win_count,
    }
    
    return render(request, 'tracker/profile.html', context)


@login_required
def competitions(request):
    """View all competitions (past and current)."""
    # Get all competitions ordered by most recent first
    all_competitions = Competition.objects.all()
    
    # Separate current, upcoming, and completed competitions
    current_comp = Competition.get_current_competition()
    completed_comps = Competition.objects.filter(status=Competition.COMPLETED)
    upcoming_comps = Competition.objects.filter(status=Competition.UPCOMING)
    
    context = {
        'current_competition': current_comp,
        'completed_competitions': completed_comps,
        'upcoming_competitions': upcoming_comps,
        'all_competitions': all_competitions,
    }
    
    return render(request, 'tracker/competitions.html', context)


@login_required
def competition_detail(request, competition_id):
    """View details of a specific competition."""
    competition = get_object_or_404(Competition, id=competition_id)
    
    # Get leaderboard for this competition
    leaderboard_data = PushupEntry.get_monthly_leaderboard(competition.year, competition.month)
    
    # Add win count to each leaderboard entry
    from django.contrib.auth.models import User
    leaderboard_with_wins = []
    for entry in leaderboard_data:
        user = User.objects.get(id=entry['user__id'])
        win_count = Competition.objects.filter(winner=user, status=Competition.COMPLETED).count()
        entry_dict = dict(entry)
        entry_dict['win_count'] = win_count
        leaderboard_with_wins.append(entry_dict)
    
    context = {
        'competition': competition,
        'leaderboard': leaderboard_with_wins,
        'participant_count': len(leaderboard_with_wins),
    }
    
    return render(request, 'tracker/competition_detail.html', context)

