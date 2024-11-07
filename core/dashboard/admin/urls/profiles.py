from django.urls import path, include
from .. import views

urlpatterns = [

    # company profile
    path("profile-edit/", views.ProfileEditView.as_view(), name="profile-edit"),
    path("profile-image-edit/", views.ProfileImageEditView.as_view(),
         name="profile-image-edit"),
    path("security-edit/", views.SecurityEditView.as_view(),
         name="security-edit"),
]
