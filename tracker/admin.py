from django.contrib import admin
from .models import PushupEntry


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

