from django import template
from accounts.models import UserType
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.conf import settings
from notifier_app.models import NotificationModel
User = get_user_model()

register = template.Library()


@register.simple_tag(takes_context=True)
def get_notifications_list(context):
    request = context.get("request")
    if request.user.is_authenticated:        
        notifications = NotificationModel.objects.filter(user=request.user,is_read=False)
        if notifications.count() >0:
            return notifications
        else:
            return None
    return None


