from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail



@shared_task
def sendEmail(template_path,email_to,subject,data):
    msg_html = render_to_string(template_path, data)

    send_mail(
        subject,
        None,
        settings.DEFAULT_FROM_EMAIL,
        [email_to],
        html_message=msg_html,
        fail_silently=True
    )
    return None