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




class CompanyOfferListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/company/offers/offer-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        queryset = OfferModel.objects.filter(
            user=self.request.user).order_by("-created_date")
        search_query = self.request.GET.get('q', None)
        ordering_query = self.request.GET.get('ordering', None)
        if search_query:
            queryset = queryset.filter(
                Q(order__order_origin__city__icontains=search_query) | Q(
                    order__order_destination__city__icontains=search_query)
                | Q(order__pk__icontains=search_query)

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


class CompanyOfferDetailView(LoginRequiredMixin, DetailView):
    template_name = "dashboard/company/offers/offer-detail.html"

    def get_queryset(self):
        return OfferModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = self.get_object()
        context['offer'] = offer
        order = self.get_object().order
        context['order_pictures'] = OrderPicture.objects.filter(order=order)
        # Retrieve the order origin
        order_origin = order.order_origin

        # Retrieve the order destination
        order_destination = order.order_destination
        context['order'] = order
        context['order_origin'] = order_origin
        context['order_destination'] = order_destination
        context["is_agreed_offer"] = True if AgreedOffer.objects.filter(is_canceled=False,offer=offer).first() else False
        context['messages_query'] = OfferMessageModel.objects.filter(offer=offer)
        return context
    
    
class CompanyOfferSendMessageView( LoginRequiredMixin, HasCompanyAccess, CreateView):
    http_method_names = ['post']
    form_class = OfferMessageForm

    def form_valid(self, form):
        # handle successful form submission
        form.instance.offer = OfferModel.objects.get(
            pk=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        messages.success(
            self.request, "message submitted successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard:company:offer-detail", kwargs={"pk": self.kwargs.get("pk")})

    def form_invalid(self, form):
        # handle unsuccessful form submission
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return redirect(self.request.META.get('HTTP_REFERER'))
