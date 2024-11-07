from django.urls import path, include
from .. import views

urlpatterns = [
    path("ticket/list/", views.TicketListView.as_view(), name="ticket-list"),
    path("ticket/<int:pk>/detail/",
         views.TicketDetailView.as_view(), name="ticket-detail"),
    path("ticket/<int:pk>/close/",
         views.TicketCloseView.as_view(), name="ticket-close"),
    path("ticket/<int:pk>/send-message/",
         views.TicketSendMessageView.as_view(), name="ticket-send-message"),
]
