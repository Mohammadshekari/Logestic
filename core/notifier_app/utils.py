from notifier_app.models import NotificationModel

def create_notification(user,title):
    try:
        NotificationModel.objects.create(
            user=user,
            title=title
        )
    except:
        pass