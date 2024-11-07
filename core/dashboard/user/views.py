from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
    View,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView
)

from accounts.models import UserType
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from orders_app.models import OrderModel, OrderOriginModel, OrderDestinationModel, OrderPicture
from dashboard.user.forms import OrderDestinationForm, OrderForm, OrderOriginForm, OrderPictureForm
from offers_app.models import OfferModel, AgreedOffer, OfferMessageModel
from profiles_app.models import UserProfile, CompanyProfile, CompanyProfileImage
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import *
from django.db.models import F, Q
from django.core import exceptions
from django.shortcuts import get_object_or_404
from dashboard.user.forms import *
from reviews_app.models import *
from orders_app.utils import calculate_google_map_distance


class OrderDetailView(DetailView):
    model = OrderModel
    template_name = 'dashboard/user/order-detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        offers = OfferModel.objects.filter(order=order)
        context['offers_total'] = offers.count()
        context['latest_offers'] = offers[:5]
        context['order_pictures'] = OrderPicture.objects.filter(order=order)
        # Retrieve the order origin
        order_origin = order.order_origin

        # Retrieve the order destination
        order_destination = order.order_destination
        context['order'] = order
        context['order_origin'] = order_origin
        context['order_destination'] = order_destination
        context['accepted_offer'] = AgreedOffer.objects.filter(
            offer__order=order, is_canceled=False).first()
        try:
            messages_query = OfferMessageModel.objects.filter(
                offer=context['accepted_offer'].offer)
        except AttributeError:
            messages_query = []
        context['messages_query'] = messages_query
        return context


class OrderOffersListView(ListView):
    template_name = 'dashboard/user/order-offers-list.html'
    paginate_by = 10

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))

    def get_queryset(self):
        search_query = self.request.GET.get('q', None)
        queryset = OfferModel.objects.filter(order=self.get_object())
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) | Q(
                    user__company_profile__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order'] = order

        return context


class OrderOffersDetailView(DetailView):
    template_name = 'dashboard/user/order-offers-detail.html'

    def get_object(self, queryset=None):
        order = get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))
        return OfferModel.objects.get(pk=self.kwargs.get("offer_id"), order=order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object().order
        context['order'] = order
        context['company_profile'] = self.get_object().user.company_profile
        context['is_accepted'] = AgreedOffer.objects.filter(
            offer=self.get_object(), is_canceled=False).exists()
        return context


class OrderOffersAcceptView(View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))
        offer = get_object_or_404(OfferModel, pk=self.kwargs.get("offer_id"))
        if AgreedOffer.objects.filter(offer__order=order, is_canceled=False).exists():
            messages.error(self.request, "order already has an accepted offer")
            return HttpResponseRedirect(reverse('dashboard:user:order-offers-detail', kwargs={"uuid": self.kwargs.get("uuid"), "pk": self.kwargs.get("offer_id")}))
        AgreedOffer.objects.create(offer=offer)
        order.status = OrderStateType.in_process.value
        order.save()
        messages.success(self.request, "successfully accepted the offer")
        return HttpResponseRedirect(reverse('dashboard:user:order-detail', kwargs={"uuid": self.kwargs.get("uuid")}))


class OrderOffersCancelView(View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))
        offer = get_object_or_404(OfferModel, pk=self.kwargs.get("offer_id"))
        agreed_offer = get_object_or_404(
            AgreedOffer, offer=offer, is_canceled=False)
        agreed_offer.is_canceled = True
        agreed_offer.save()
        order.status = OrderStateType.in_process.value
        order.save()

        messages.success(self.request, "offer has canceled successfully")
        return HttpResponseRedirect(reverse('dashboard:user:order-detail', kwargs={"uuid": self.kwargs.get("uuid")}))


class OrderPicturesView(CreateView):
    template_name = 'dashboard/user/order-pictures.html'
    form_class = OrderPictureForm

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))

    def form_valid(self, form):
        form.instance.order = self.get_object()
        if OrderPicture.objects.filter(order=self.get_object()).count() >= 6:
            form.add_error(
                None, "Maximum limit of 6 items reached for this order.")
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order'] = order
        context['order_pictures'] = OrderPicture.objects.filter(order=order)
        return context

    def get_success_url(self):
        # Specify the URL or route name you want to redirect to
        return reverse('dashboard:user:order-pictures', kwargs={'uuid': self.get_object().uuid})


class OrderPicturesDeleteView(View):

    def get_object(self, queryset=None):
        order = get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))
        picture_id = self.kwargs.get("picture_id")
        return get_object_or_404(OrderPicture, id=picture_id, order=order)

    def get(self, request, *args, **kwargs):
        picture = self.get_object()
        order_uuid = picture.order.uuid
        picture.delete()
        return redirect(reverse('dashboard:user:order-pictures', kwargs={'uuid': order_uuid}))


class OrderEditView(TemplateView):
    template_name = 'dashboard/user/order-edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_origin = order.order_origin
        order_destination = order.order_destination
        context['order_form'] = OrderForm(instance=order)
        context['order_origin_form'] = OrderOriginForm(instance=order_origin)
        context['order_destination_form'] = OrderDestinationForm(
            instance=order_destination)
        return context


class CompanyPreviewView(DetailView):
    template_name = 'dashboard/user/company-profile-preview.html'
    model = CompanyProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_images"] = CompanyProfileImage.objects.filter(
            profile=self.get_object())
        context["reviews_query"] = ReviewModel.objects.filter(company=self.get_object().user)
        return context


class OrderBasicInfoEditView(View):

    success_message = "basic info have been updated"

    form_class = OrderForm

    def get_redirect_url(self):
        return reverse('dashboard:user:order-edit', kwargs={"uuid": self.get_object().uuid})

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.get_redirect_url())
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'Error in {field}: {error}')
            return redirect(self.get_redirect_url())


class OrderOriginDetailEditView(View):

    success_message = "order origin info have been updated"

    form_class = OrderOriginForm

    def get_redirect_url(self):
        return reverse('dashboard:user:order-edit', kwargs={"uuid": self.get_object().order.uuid})

    def get_object(self, queryset=None):
        return OrderOriginModel.objects.get(order__uuid=self.kwargs.get("uuid"))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            origin_object = form.save()
            messages.success(request, self.success_message)
            calculate_google_map_distance(origin_object.order)
            return redirect(self.get_redirect_url())
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'Error in {field}: {error}')
            return redirect(self.get_redirect_url())


class OrderDestinationDetailEditView(View):
    http_method_names = ['post']
    success_message = "order destination info have been updated"
    form_class = OrderDestinationForm

    def get_redirect_url(self):
        return reverse('dashboard:user:order-edit', kwargs={"uuid": self.get_object().order.uuid})

    def get_object(self, queryset=None):
        return OrderDestinationModel.objects.get(order__uuid=self.kwargs.get("uuid"))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            destination_object = form.save()
            messages.success(request, self.success_message)
            calculate_google_map_distance(destination_object.order)
            return redirect(self.get_redirect_url())
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'Error in {field}: {error}')
            return redirect(self.get_redirect_url())


class OrderCloseView(View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))
        order.is_done = True
        order.status = OrderStateType.done.value
        order.save()
        
        messages.success(self.request, "order was successfully closed")
        accepted_offer = AgreedOffer.objects.filter(
            offer__order=order, is_canceled=False).first()
        print("company :",accepted_offer.offer.user)
        return HttpResponseRedirect(reverse('dashboard:user:order-offers-review', kwargs={"uuid": self.kwargs.get("uuid"), "offer_id": accepted_offer.offer.pk}))


class OrderOffersReviewView(CreateView,SuccessMessageMixin):
    template_name = 'dashboard/user/order-offers-review.html'
    model = ReviewModel
    fields = ["email",'rate','description',"company"]
    success_message = "thanks for your review about the company"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))
        offer = get_object_or_404(OfferModel, id=self.kwargs.get("offer_id"))
        context['order'] = order
        context['offer'] = offer
        context['company_profile'] = offer.user.company_profile
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:user:order-detail', kwargs={"uuid": self.kwargs.get("uuid")})
    
class UserOfferSendMessageView(CreateView):
    http_method_names = ['post']
    form_class = OfferMessageForm

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, uuid=self.kwargs.get("uuid"))

    def form_valid(self, form):
        # handle successful form submission
        offer = OfferModel.objects.get(
            pk=self.kwargs.get("offer_id"))
        form.instance.offer = offer
        form.instance.email = offer.order.email
        messages.success(
            self.request, "message submitted successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:user:order-detail', kwargs={"uuid": self.get_object().uuid})

    def form_invalid(self, form):
        # handle unsuccessful form submission
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return reverse('dashboard:user:order-detail', kwargs={"uuid": self.get_object().uuid})
