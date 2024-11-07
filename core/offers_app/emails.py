from utils.email.email_utils import send_styled_email
from accounts.jwt_mixins import create_jwt_token
from django.conf import settings


def get_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain
def get_protocol():
    # Determine the protocol based on the SECURE_SSL_REDIRECT setting
    return'https' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'http'
  

def send_offer_notify_to_user(to_email, order, company_profile, offer):
    subject = "New Offer"
    template_name = "emails/user/user-offer-notify.html"
    context = {"email": to_email, "company_profile": company_profile,
               "offer": offer, "order": order, "fullname": order.get_fullname()}              
    context.update({"domain":get_domain(),"protocol":get_protocol()})
    send_styled_email(subject, template_name, context, to_email)


def send_offer_accepted_to_company(to_email, order, company_profile, offer):
    subject = "Your Offer has been accepted"
    template_name = "emails/company/company-offer-accepted.html"
    context = {"email": to_email, "company_profile": company_profile, "offer": offer,
               "order": order, "jwt_token": create_jwt_token(company_profile.user.id)}
    context.update({"domain":get_domain(),"protocol":get_protocol()})
    send_styled_email(subject, template_name, context, to_email)


def send_offer_canceled_to_company(to_email, order, company_profile, offer):
    subject = "Your Offer has been canceled"
    template_name = "emails/company/company-offer-canceled.html"
    context = {"email": to_email, "company_profile": company_profile, "offer": offer,
               "order": order, "jwt_token": create_jwt_token(company_profile.user.id)}
    context.update({"domain":get_domain(),"protocol":get_protocol()})
    send_styled_email(subject, template_name, context, to_email)
