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
from orders_app.models import OrderModel, OrderOriginModel, OrderDestinationModel, OrderStateType, OrderPicture
from offers_app.models import OfferModel, OfferTemplateModel
from offers_app.forms import OfferTemplateForm, OfferForm
from profiles_app.models import CompanyProfile ,CompanyServicesType,PaymentMethodsType
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from dashboard.company.forms import *
from django.db.models import F, Q
from django.core import exceptions

from django.contrib.auth.views import PasswordChangeView
from dashboard.company.forms import CompanyChangePasswordForm

class ProfileEditView(LoginRequiredMixin,SuccessMessageMixin,HasCompanyAccess, UpdateView):
    template_name = "dashboard/company/profiles/profile-edit.html"
    form_class = CompanyProfileForm
    success_message = "profile details updated successfully"
    success_url = reverse_lazy("dashboard:company:profile-edit")
    
    def get_object(self, queryset=None):
        return CompanyProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = CompanyProfileImageForm(instance=self.get_object())
        context['service_types'] = [{"id": item[0], "title": item[1]} for item in CompanyServicesType.choices]
        context['payment_types'] = [{"id": item[0], "title": item[1]} for item in PaymentMethodsType.choices]
        return context

    
    
class ProfileImageEditView(LoginRequiredMixin,SuccessMessageMixin,HasCompanyAccess, UpdateView):
    http_method_names = ['post']
    form_class = CompanyProfileImageForm
    success_message = "profile image updated successfully"

    def get_object(self, queryset=None):
        return CompanyProfile.objects.get(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("dashboard:company:profile-edit")
    

class SecurityEditView(LoginRequiredMixin,SuccessMessageMixin,HasCompanyAccess,PasswordChangeView):
    form_class = CompanyChangePasswordForm
    success_message = "your password has been changed successfully"
    success_url = reverse_lazy('dashboard:company:security-edit')
    template_name = "dashboard/company/profiles/security-edit.html"