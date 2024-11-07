from utils.email.email_utils import send_styled_email
from django.conf import settings
from accounts.jwt_mixins import create_jwt_token

def get_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain
def get_protocol():
    # Determine the protocol based on the SECURE_SSL_REDIRECT setting
    return'https' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'http'

def send_company_welcome(to_email,user):
    subject = "Welcome to NettiMutto"
    template_name = "emails/company/company-welcome.html"
    context = {"email":to_email}
    context.update({"domain":get_domain(),"protocol":get_protocol(),"jwt_token":create_jwt_token(user.id)})
    send_styled_email(subject, template_name, context, to_email)