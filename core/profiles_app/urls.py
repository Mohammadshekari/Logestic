from django.urls import path, include, re_path
from . import views
app_name = "profiles"

urlpatterns = [
    # api for orders
    path("api/v1/", include("profiles_app.api.v1.urls")),
    
    # add company
    path("add-company/",views.AddCompanyView.as_view(),name="add-company"),
    path("add-company/completed/",views.AddCompanyCompletedView.as_view(),name="add-company-completed")
]
