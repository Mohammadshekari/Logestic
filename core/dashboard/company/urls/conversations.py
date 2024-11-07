from django.urls import path, include
from .. import views

urlpatterns = [
    path("conversation/list/", views.ConversationListView.as_view(), name="conversation-list"),
    
]
