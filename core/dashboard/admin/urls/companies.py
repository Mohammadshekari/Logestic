from django.urls import path, include
from .. import views

urlpatterns = [
    # company-profiles management urls
    path("company/list/", views.CompanyProfileListView.as_view(),
         name="company-profile-list"),
    path("company/<int:pk>/edit/",
         views.CompanyProfileEditView.as_view(), name="company-profile-edit"),
    # path("company/<int:pk>/change-state/",
    #      views.CompanyProfileChangeStateView.as_view(), name="company-profile-change-state"),
]
