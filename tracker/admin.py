from django.contrib import admin
from .models import PushupEntry, Competition


@admin.register(PushupEntry)
class PushupEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'count', 'created_at')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('created_at', 'updated_at')
        return ('created_at', 'updated_at')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_date', 'end_date', 'winner', 'winner_total', 'days_remaining')
    list_filter = ('status', 'start_date')
    search_fields = ('name', 'winner__username')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Competition Info', {
            'fields': ('name', 'start_date', 'end_date', 'status')
        }),
        ('Winner', {
            'fields': ('winner', 'winner_total'),
            'description': 'Winner is automatically determined when competition ends'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['update_status', 'determine_winners']
    
    def update_status(self, request, queryset):
        """Update status of selected competitions."""
        for competition in queryset:
            competition.update_status()
        self.message_user(request, f'Updated status for {queryset.count()} competition(s)')
    update_status.short_description = 'Update competition status'
    
    def determine_winners(self, request, queryset):
        """Determine winners for completed competitions."""
        count = 0
        for competition in queryset:
            if competition.status == Competition.COMPLETED and not competition.winner:
                competition.determine_winner()
                count += 1
        self.message_user(request, f'Determined winners for {count} competition(s)')
    determine_winners.short_description = 'Determine winners'

