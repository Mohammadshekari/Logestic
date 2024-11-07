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

from profiles_app.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from dashboard.admin.forms import *
from django.db.models import F, Q
from django.core import exceptions


class CompanyProfileListView(LoginRequiredMixin, HasAdminAccess, ListView):
    template_name = "dashboard/admin/companies/company-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        queryset = CompanyProfile.objects.filter().order_by("-created_date")
        search_query = self.request.GET.get('q', None)
        ordering_query = self.request.GET.get('ordering', None)
        if search_query:
            queryset = queryset.filter(user__icontains=search_query)
        if ordering_query:
            try:
                queryset = queryset.order_by(ordering_query)
            except exceptions.FieldError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_result"] = self.get_queryset().count()
        return context


class CompanyProfileEditView(LoginRequiredMixin, SuccessMessageMixin, HasAdminAccess, UpdateView):
    template_name = "dashboard/admin/companies/company-edit.html"
    queryset = CompanyProfile.objects.all()
    form_class= AdminCompanyProfileForm
    success_message = "profile details updated successfully"

    def get_success_url(self) -> str:
        return reverse_lazy("dashboard:admin:company-profile-edit",kwargs={"pk":self.kwargs.get("pk")})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_types'] = [
            {"id": item[0], "title": item[1]} for item in CompanyServicesType.choices]
        context['payment_types'] = [
            {"id": item[0], "title": item[1]} for item in PaymentMethodsType.choices]
        context['status_types'] = [
            {"id": item[0], "title": item[1]} for item in CompanyProfileStatusType.choices]
        return context
