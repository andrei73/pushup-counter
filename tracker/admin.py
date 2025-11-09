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
            'description': 'Winner is automatically determined when status is changed to "completed"'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['update_status', 'determine_winners']
    
    def save_model(self, request, obj, form, change):
        """Override save to automatically determine winner when status changes to completed."""
        # Check if status changed to completed
        if change:  # Only for existing objects
            # Get the old object from database
            old_obj = Competition.objects.get(pk=obj.pk)
            # If status changed to completed and no winner set
            if obj.status == Competition.COMPLETED and old_obj.status != Competition.COMPLETED:
                # Save first to update the status
                super().save_model(request, obj, form, change)
                # Then determine winner
                if not obj.winner:
                    obj.determine_winner()
                    self.message_user(request, f'Winner automatically determined: {obj.winner} with {obj.winner_total} pushups')
                return
        # Normal save for other cases
        super().save_model(request, obj, form, change)
    
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
            if competition.status == Competition.COMPLETED:
                if not competition.winner:
                    competition.determine_winner()
                    count += 1
                    self.message_user(request, f'✅ Determined winner for {competition.name}: {competition.winner} ({competition.winner_total} pushups)', level='success')
                else:
                    self.message_user(request, f'ℹ️ {competition.name} already has a winner: {competition.winner}', level='info')
            else:
                self.message_user(request, f'⚠️ {competition.name} is not completed yet (status: {competition.status})', level='warning')
        
        if count > 0:
            self.message_user(request, f'Successfully determined winners for {count} competition(s)')
        else:
            self.message_user(request, 'No competitions needed winner determination')
    determine_winners.short_description = 'Determine winners for completed competitions'

