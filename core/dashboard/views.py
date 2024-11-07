from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView,View
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

# Create your views here.
class DashboardHomeView(LoginRequiredMixin, View):
    """
    a class based view to show index page
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('accounts:login'))
        if self.request.user.type == UserType.admin.value:
            return redirect(reverse_lazy('dashboard:admin:home'))
        if self.request.user.type == UserType.company.value:
            return redirect(reverse_lazy('dashboard:company:home'))
        return super().dispatch(request, *args, **kwargs)

