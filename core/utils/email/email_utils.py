from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_styled_email(subject, template_name, context, to_email):
    html_content = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL, 
        to=[to_email],
    )
    email.content_subtype = 'html'
    email.mixed_subtype = 'related'
    email.send()
