from django.contrib import admin
from invoices_app.models import *
# Register your models here.


@admin.register(InvoiceModel)
class InvoiceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'invoice_number','total_amount', 'created_date']
