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
        from django.db.models import Sum, Avg, Max
        
        entries = PushupEntry.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )
        
        stats = entries.aggregate(
            total=Sum('count'),
            average=Avg('count'),
            best_day=Max('count')
        )
        
        stats['total'] = stats['total'] or 0
        stats['average'] = round(stats['average'], 1) if stats['average'] else 0
        stats['best_day'] = stats['best_day'] or 0
        stats['days_active'] = entries.values('date').distinct().count()
        
        return stats

