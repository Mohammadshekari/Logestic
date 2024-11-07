from django.contrib import admin
from tickets_app.models import *

# Register your models here.


@admin.register(AttachmentModel)
class AttachmentAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "file")


@admin.register(TicketModel)
class TicketAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "user", "status", "title")
    search_fields = ["title", "description"]


@admin.register(TicketMessageModel)
class TicketMessageAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "user", "ticket","is_support")
    search_fields = ["description"]
