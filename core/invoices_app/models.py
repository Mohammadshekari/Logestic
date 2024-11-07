from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import string
from .emails import *
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class InvoiceStatusType(models.IntegerChoices):
    pending = 1, _("pending")
    payed = 2, _("payed")


def generate_invoice_number():
    # Generate a random alphanumeric string of length 10
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Create your models here.


class InvoiceModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    orders = models.ManyToManyField('orders_app.OrderModel')
    invoice_number = models.CharField(
        max_length=10, unique=True, default=generate_invoice_number)
    state = models.IntegerField(
        choices=InvoiceStatusType.choices, default=InvoiceStatusType.pending)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    total_tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    final_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)

    deadline_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def tax_amount(self):
        # Ensure TAX_AMOUNT is used as a Decimal
        return Decimal(settings.TAX_AMOUNT)

    def calculate_total_cost(self):
        total_cost = sum(Decimal(order.price) for order in self.orders.all())
        return total_cost

    def calculate_total_tax(self):
        # Use Decimal to perform precise arithmetic
        total_cost = self.calculate_total_cost()
        total_tax = total_cost * (self.tax_amount / Decimal(100))
        return round(total_tax,ndigits=2)
    


@receiver(post_save, sender=InvoiceModel)
def invoice_created_for_company(sender, instance, created, **kwargs):
    if created:
        send_company_invoice_notify(instance.user.email, instance)
