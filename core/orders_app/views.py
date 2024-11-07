from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView, View
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


from accounts.models import UserType
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from .forms import *
from django.http import HttpResponseRedirect
from orders_app.utils import calculate_google_map_distance
# Create your views here.
class AddOrderView(FormView):
    template_name = "mixins/add-order.html"
    form_class = AddOrderForm

    def form_valid(self, form):
        # print(self.request.POST)
        order_form = OrderForm(data=self.request.POST)
        if order_form.is_valid():
            order_instance = order_form.save()
        else:
            # print(order_form.errors)
            pass
            
        origin_form = OrderOriginForm(data=self.request.POST,prefix="origin")
        if origin_form.is_valid():
            origin_form.instance.pk = order_instance.id
            origin_form.instance.order = order_instance
            origin_form.save()
        else:
            # print(origin_form.errors)
            pass
        destination_form = OrderDestinationForm(data=self.request.POST,prefix="destination")
        if destination_form.is_valid():
            destination_form.instance.pk = order_instance.id
            destination_form.instance.order = order_instance
            destination_form.save()
        else:
            # print(destination_form.errors)
            pass
        calculate_google_map_distance(order_instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:add-order-completed')


class AddOrderCompletedView(TemplateView):
    template_name = "mixins/add-order-completed.html"
