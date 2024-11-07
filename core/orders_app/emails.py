from utils.email.email_utils import send_styled_email
from accounts.jwt_mixins import create_jwt_token
from django.conf import settings


def get_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain


def get_protocol():
    # Determine the protocol based on the SECURE_SSL_REDIRECT setting
    return 'https' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'http'


def send_order_created_to_user(to_email, order):
    subject = f"Order Submitted #{order.id}"
    template_name = "emails/user/user-order-created.html"
    context = {"email": to_email, "order": order, "fullname": order.get_fullname(
    ), "origin": order.order_origin, "destination": order.order_destination}
    context.update({"domain": get_domain(), "protocol": get_protocol()})
    send_styled_email(subject, template_name, context, to_email)
