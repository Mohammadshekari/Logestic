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
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from dashboard.company.forms import *


class DashboardHomeView(LoginRequiredMixin, HasCompanyAccess, TemplateView):
    """
    a class based view to show index page
    """

    template_name = "dashboard/company/home.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
