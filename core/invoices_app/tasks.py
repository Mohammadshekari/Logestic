from invoices_app.models import InvoiceModel
from offers_app.models import OfferModel, AgreedOffer
from orders_app.models import OrderModel
from accounts.models import UserType
from django.contrib.auth import get_user_model
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


User = get_user_model()


@shared_task(name="generate_invoices")
def generate_invoices():
    print("Periodic Task Triggered")

    # Get the current date and time
    now = timezone.now()

    # Get the current year and month
    current_year = now.year
    current_month = now.month

    # Query all company users
    company_users = User.objects.filter(type=UserType.company.value)
    for company_user in company_users:
        # Query all offers that happened in the entire current month
        agreed_offers = AgreedOffer.objects.filter(
            offer__user=company_user,
            created_date__year=current_year,
            created_date__month=current_month,
            is_canceled=False
        )
        invoice_obj, created = InvoiceModel.objects.update_or_create(
            user=company_user,
            month=current_month,
            year=current_year,
            defaults={'deadline_date': now + timedelta(days=7)}
        )

        try:
            # Add orders to the invoice (m2m field)
            orders = [agreed_offer.offer.order for agreed_offer in agreed_offers]
            invoice_obj.orders.add(*orders)

            # Calculate and update the total amount
            total_amount = sum(order.price for order in orders)
            tax_amount = (total_amount * (invoice_obj.tax_amount / 100))
            invoice_obj.total_amount = total_amount
            invoice_obj.total_tax_amount = tax_amount
            invoice_obj.final_amount = total_amount + tax_amount
            # Only update total_amount here
            invoice_obj.save(
                update_fields=['total_amount', "total_tax_amount", "final_amount"])
        except Exception as e:
            raise e
