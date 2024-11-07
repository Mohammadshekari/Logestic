from django.urls import path, include, re_path
from profiles_app.api.v1 import views

urlpatterns = [
      path(
        "create-company-profile",
        views.CreateCompanyProfileModelViewSet.as_view(
            {"post": "create",}),
        name="create-company-profile",
    ),
    
]