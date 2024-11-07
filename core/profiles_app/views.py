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
from .forms import AddCompanyForm

# Create your views here.
class AddCompanyView(FormView):
    template_name = "mixins/add-company.html"
    form_class = AddCompanyForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profiles:add-company-completed')


class AddCompanyCompletedView(TemplateView):
    template_name = "mixins/add-company-completed.html"
