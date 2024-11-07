from typing import Any, Dict
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
    View
)
from meta.views import MetadataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from django.db.models import F,Q
from django.core import exceptions
from django.contrib.auth import get_user_model
from notifier_app.models import *

User = get_user_model()
