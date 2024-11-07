from django.urls import path, include
from notifier_app import views
app_name = "notifier_app"

urlpatterns = [
    path("api/v1/", include("notifier_app.api.v1.urls")),
]