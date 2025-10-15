from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


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

