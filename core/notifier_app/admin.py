from django.contrib import admin
from .models import *

class NotificationAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "user", "title", "is_read","created_date")
    list_filter = ("user", "created_date")
    search_fields = ["title", "content"]



admin.site.register(NotificationModel, NotificationAdmin)