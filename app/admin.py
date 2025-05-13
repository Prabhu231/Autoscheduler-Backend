from django.contrib import admin
from .models import User, ScheduledEmail, EmailAttachment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'blacklist_token')
    search_fields = ('email',)
    list_filter = ('email',)
    ordering = ('id',)


@admin.register(ScheduledEmail)
class ScheduledEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'scheduled_at', 'status', 'created_at', 'updated_at')
    search_fields = ('subject', 'recipients')
    list_filter = ('status', 'is_html', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'size', 'content_type', 'created_at')
    search_fields = ('name', 'content_type')
    list_filter = ('content_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

