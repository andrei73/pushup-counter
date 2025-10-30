from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import date
from calendar import monthrange


class Competition(models.Model):
    """Model to track monthly pushup competitions."""
    UPCOMING = 'upcoming'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (UPCOMING, 'Upcoming'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    ]
    
    name = models.CharField(max_length=100, help_text="e.g., 'October 2025'")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UPCOMING)
    winner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='competitions_won'
    )
    winner_total = models.IntegerField(null=True, blank=True, help_text="Total pushups by winner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Competitions"
    
    def __str__(self):
        return f"{self.name} ({self.status})"
    
    @property
    def year(self):
        """Get the year of the competition."""
        return self.start_date.year
    
    @property
    def month(self):
        """Get the month of the competition."""
        return self.start_date.month
    
    @property
    def days_remaining(self):
        """Calculate days remaining in the competition."""
        if self.status == self.COMPLETED:
            return 0
        today = date.today()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days + 1
    
    @property
    def is_active(self):
        """Check if competition is currently active."""
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def update_status(self):
        """Update competition status based on current date."""
        today = date.today()
        if today < self.start_date:
            self.status = self.UPCOMING
        elif today > self.end_date:
            self.status = self.COMPLETED
            if not self.winner:
                self.determine_winner()
        else:
            self.status = self.ACTIVE
        self.save()
    
    def determine_winner(self):
        """Determine and set the winner of the competition."""
        from django.db.models import Sum
        
        # Get the top performer for this competition's month
        entries = PushupEntry.objects.filter(
            date__year=self.year,
            date__month=self.month
        ).values('user').annotate(
            total=Sum('count')
        ).order_by('-total').first()
        
        if entries:
            self.winner_id = entries['user']
            self.winner_total = entries['total']
            self.save()
    
    @classmethod
    def get_current_competition(cls):
        """Get the currently active competition."""
        today = date.today()
        competition = cls.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).first()
        
        if competition:
            competition.update_status()
        
        return competition
    
    @classmethod
    def get_last_completed_competition(cls):
        """Get the most recent completed competition."""
        return cls.objects.filter(status=cls.COMPLETED).first()
    
    @classmethod
    def create_monthly_competition(cls, year, month):
        """Create a competition for a specific month."""
        # Get first and last day of the month
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Generate name (e.g., "October 2025")
        name = first_day.strftime("%B %Y")
        
        # Check if competition already exists
        if cls.objects.filter(start_date=first_day).exists():
            return cls.objects.get(start_date=first_day)
        
        # Create new competition
        competition = cls.objects.create(
            name=name,
            start_date=first_day,
            end_date=last_day,
            status=cls.UPCOMING
        )
        
        competition.update_status()
        return competition


class PushupEntry(models.Model):
    """Model to track pushup entries for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pushup_entries')
    date = models.DateField(default=timezone.now)
    count = models.IntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = "Pushup Entries"
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.count} pushups on {self.date}"

    @staticmethod
    def get_monthly_leaderboard(year, month):
        """Get leaderboard for a specific month."""
        from django.db.models import Sum
        
        entries = PushupEntry.objects.filter(
            date__year=year,
            date__month=month
        ).values('user__id', 'user__username', 'user__first_name', 'user__last_name').annotate(
            total_pushups=Sum('count')
        ).order_by('-total_pushups')
        
        return entries

    @staticmethod
    def get_user_monthly_total(user, year, month):
        """Get total pushups for a user in a specific month."""
        from django.db.models import Sum
        
        total = PushupEntry.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('count'))['total']
        
        return total or 0

    @staticmethod
    def get_user_stats(user, year, month):
        """Get statistics for a user in a specific month."""
        from django.db.models import Sum, Max
        
        entries = PushupEntry.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )
        
        # Get daily totals (sum multiple entries per day)
        daily_totals = entries.values('date').annotate(
            day_total=Sum('count')
        ).values_list('day_total', flat=True)
        
        # Calculate stats
        total = sum(daily_totals) if daily_totals else 0
        days_active = len(daily_totals)
        best_day = max(daily_totals) if daily_totals else 0
        average = round(total / days_active, 1) if days_active > 0 else 0
        
        stats = {
            'total': total,
            'average': average,
            'best_day': best_day,
            'days_active': days_active
        }
        
        return stats

