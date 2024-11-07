from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
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
from invoices_app.models import InvoiceModel
from profiles_app.models import CompanyProfile, CompanyServicesType, PaymentMethodsType
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from dashboard.company.forms import *
from django.db.models import F, Q
from django.core import exceptions
from dashboard.admin.forms import InvoiceStateForm

class CompanyInvoiceListView(LoginRequiredMixin,HasAdminAccess, ListView):
    template_name = "dashboard/admin/invoices/invoice-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        queryset = InvoiceModel.objects.all().order_by("-created_date")
        search_query = self.request.GET.get('q', None)
        ordering_query = self.request.GET.get('ordering', None)
        if search_query:
            queryset = queryset.filter(
                Q(invoice_number=search_query)
            )
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


class CompanyInvoiceDetailView(LoginRequiredMixin, HasAdminAccess,SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/invoices/invoice-detail.html"
    form_class = InvoiceStateForm
    success_message = "Updated Invoice States"

    def get_object(self):
        return get_object_or_404(InvoiceModel, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def get_success_url(self):
        # Redirect back to the current page
        return self.request.path