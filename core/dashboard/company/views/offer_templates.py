from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse,JsonResponse
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
    View
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




class CompanyOfferTemplateListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/company/offer_templates/offer-template-list.html"

    def get_queryset(self):
        return OfferTemplateModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CompanyOfferTemplateEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "dashboard/company/offer_templates/offer-template-edit.html"
    model = OfferTemplateModel
    form_class = OfferTemplateForm
    success_message = "offer template updated successfully"

    def get_queryset(self):
        return OfferTemplateModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self) -> str:
        # Get the ID of the newly created object
        object_id = self.object.id
        # Build the URL for the edit page using the ID
        return reverse('dashboard:company:offer-template-edit', kwargs={'pk': object_id})


class CompanyOfferTemplateCreateView(LoginRequiredMixin, CreateView):
    template_name = "dashboard/company/offer_templates/offer-template-create.html"
    model = OfferTemplateModel
    form_class = OfferTemplateForm
    success_message = "your offer template has been set successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        # Get the ID of the newly created object
        object_id = self.object.id
        # Build the URL for the edit page using the ID
        return reverse('dashboard:company:offer-template-edit', kwargs={'pk': object_id})


class CompanyOfferTemplateDeleteView(LoginRequiredMixin, DeleteView):
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('dashboard:company:offer-template-list')

    def get_object(self, queryset=None):
        return OfferTemplateModel.objects.get(user=self.request.user, pk=self.kwargs.get("pk"))
    


class CompanyOfferTemplateDetailJsonView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        # Attempt to retrieve the offer template object or return a 404
        offer_template = get_object_or_404(OfferTemplateModel, user=request.user, pk=pk)
        
        # Structure the JSON response data
        data = {
            "id": offer_template.id,
            "title": offer_template.title,
            "description": offer_template.description,
            # Add any other fields needed here
        }
        
        return JsonResponse(data)
