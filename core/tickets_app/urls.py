from django.urls import path, include, re_path

app_name = "tickets"

urlpatterns = [
    # api for orders
    path("api/v1/", include("tickets_app.api.v1.urls"))
]
