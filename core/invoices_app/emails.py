
from utils.email.email_utils import send_styled_email
from accounts.jwt_mixins import create_jwt_token
from django.conf import settings


def get_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain


def get_protocol():
    # Determine the protocol based on the SECURE_SSL_REDIRECT setting
    return 'https' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'http'


def send_company_invoice_notify(to_email, invoice):
    subject = f" Invoice Created - Action Required"
    template_name = "emails/company/company-invoice-created.html"
    context = {"email": to_email, "invoice": invoice,
               "company_profile": invoice.user.profile}
    context.update({"domain": get_domain(), "protocol": get_protocol()})
    send_styled_email(subject, template_name, context, to_email)
