from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('notification/', views.NotificationListApiView.as_view(),
         name='notification-list'),
    path('notification/unread/', views.NotificationListUnreadApiView.as_view(),
         name='notification-unread-list'),
    path('notification/mark-as-read/', views.NotificationMarkAsReadApiView.as_view(),
         name='notification-mark-as-read'),
    path('notification/mark-as-read/all/', views.NotificationMarkAsReadAllApiView.as_view(),
         name='notification-mark-as-read-all')
]
