from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)


from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from profiles_app.models import AdminProfile
from dashboard.admin.forms import AdminProfileForm,AdminProfileImageForm

from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from django.db.models import F, Q
from django.core import exceptions
from django.contrib.auth.views import PasswordChangeView
from dashboard.admin.forms import AdminChangePasswordForm


class ProfileEditView(LoginRequiredMixin,SuccessMessageMixin,HasAdminAccess, UpdateView):
    template_name = "dashboard/admin/profiles/profile-edit.html"
    form_class = AdminProfileForm
    success_message = "profile details updated successfully"
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    
    def get_object(self, queryset=None):
        return AdminProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = AdminProfileImageForm(instance=self.get_object())
        return context

    
    
class ProfileImageEditView(LoginRequiredMixin,SuccessMessageMixin,HasAdminAccess, UpdateView):
    http_method_names = ['post']
    form_class = AdminProfileImageForm
    success_message = "profile image updated successfully"

    def get_object(self, queryset=None):
        return AdminProfile.objects.get(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("dashboard:admin:profile-edit")

class SecurityEditView(LoginRequiredMixin,SuccessMessageMixin,HasAdminAccess,PasswordChangeView):
    form_class = AdminChangePasswordForm
    success_message = "your password has been changed successfully"
    success_url = reverse_lazy('dashboard:admin:security-edit')
    template_name = "dashboard/admin/profiles/security-edit.html"