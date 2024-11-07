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
from tickets_app.models import TicketModel,TicketMessageModel
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from dashboard.company.forms import *
from django.db.models import F, Q
from django.core import exceptions


class TicketListView( LoginRequiredMixin, HasCompanyAccess, ListView):
    template_name = "dashboard/company/tickets/ticket-list.html"
    paginate_by = 10
    ordering = "-created_date"

    def get_queryset(self):
        queryset = TicketModel.objects.filter(
            user=self.request.user).order_by("-created_date")
        search_query = self.request.GET.get('q', None)
        ordering_query = self.request.GET.get('ordering', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
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


class TicketCreateView( LoginRequiredMixin, HasCompanyAccess, SuccessMessageMixin, CreateView):

    template_name = "dashboard/company/tickets/ticket-create.html"
    form_class = TicketCompanyForm
    success_message = "ticket has been created successfully"
    success_url = reverse_lazy("dashboard:company:ticket-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user).order_by("-created_date")


class TicketDetailView( LoginRequiredMixin, HasCompanyAccess, DetailView):
    template_name = "dashboard/company/tickets/ticket-detail.html"

    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user).order_by("-created_date")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages_query"] = TicketMessageModel.objects.filter(
            ticket__id=self.kwargs.get("pk")).order_by("created_date")
        return context



class TicketSendMessageView( LoginRequiredMixin, HasCompanyAccess, CreateView):
    http_method_names = ['post']
    form_class = TicketMessageForm

    def form_valid(self, form):
        # handle successful form submission
        form.instance.ticket = TicketModel.objects.get(
            pk=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        messages.success(
            self.request, "message submitted successfully")
        ticket = form.instance.ticket
        ticket.status = TicketStatusType.support_pending.value
        ticket.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard:company:ticket-detail", kwargs={"pk": self.kwargs.get("pk")})

    def form_invalid(self, form):
        # handle unsuccessful form submission
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return redirect(self.request.META.get('HTTP_REFERER'))
