from django.urls import path, include
from .. import views


urlpatterns = [
    # company dashboard 
    path("home/", views.DashboardHomeView.as_view(), name="home"),
]