from django.contrib import admin

from .models import Session, Message

class SessionAdmin(admin.ModelAdmin):
    list_display = 'id', 'ip', 'user', 'replied', 'finished', 'started', 'updated'
    list_filter = 'started', 'replied', 'finished'
    readonly_fields = 'id', 'user', 'ip'

    change_form_template = 'sepiida_chat/admin_session_change_view.html'

admin.site.register(Session, SessionAdmin)
