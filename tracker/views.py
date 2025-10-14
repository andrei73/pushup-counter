from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from .models import PushupEntry
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
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    today = now.date()
    
    # Get user's monthly stats
    stats = PushupEntry.get_user_stats(request.user, current_year, current_month)
    
    # Get today's pushup count
    today_total = PushupEntry.objects.filter(
        user=request.user,
        date=today
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
    
    context = {
        'stats': stats,
        'today_total': today_total,
        'recent_entries': recent_entries,
        'user_rank': user_rank,
        'total_competitors': leaderboard.count(),
        'current_month': now.strftime('%B %Y'),
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    
    return render(request, 'tracker/dashboard.html', context)


@login_required
def leaderboard(request):
    """Leaderboard view showing all users' rankings."""
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    
    # Get monthly leaderboard
    leaderboard_data = PushupEntry.get_monthly_leaderboard(current_year, current_month)
    
    context = {
        'leaderboard': leaderboard_data,
        'current_month': now.strftime('%B %Y'),
        'current_user_id': request.user.id,
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
    entries = PushupEntry.objects.filter(user=request.user)
    
    # Get filter parameters
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year:
        entries = entries.filter(date__year=year)
    if month:
        entries = entries.filter(date__month=month)
    
    # Get available years for filter dropdown
    years = PushupEntry.objects.filter(user=request.user).dates('date', 'year', order='DESC')
    
    context = {
        'entries': entries,
        'years': years,
        'selected_year': year,
        'selected_month': month,
    }
    
    return render(request, 'tracker/history.html', context)


@login_required
def profile(request, username=None):
    """View a user's profile and stats."""
    from django.contrib.auth.models import User
    
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    
    # Get user's stats
    stats = PushupEntry.get_user_stats(profile_user, current_year, current_month)
    
    # Get user's rank
    leaderboard = PushupEntry.get_monthly_leaderboard(current_year, current_month)
    user_rank = None
    for idx, entry in enumerate(leaderboard, 1):
        if entry['user__id'] == profile_user.id:
            user_rank = idx
            break
    
    # Get recent entries
    recent_entries = PushupEntry.objects.filter(user=profile_user)[:10]
    
    context = {
        'profile_user': profile_user,
        'stats': stats,
        'user_rank': user_rank,
        'recent_entries': recent_entries,
        'current_month': now.strftime('%B %Y'),
        'is_own_profile': profile_user == request.user,
    }
    
    return render(request, 'tracker/profile.html', context)

