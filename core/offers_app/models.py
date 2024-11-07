from django.dispatch import receiver
from .emails import *
from django.db.models.signals import post_save
from django.db import models
from orders_app.models import OrderModel
from django.contrib.auth import get_user_model
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator

User = get_user_model()
# Create your models here.


class OfferModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_user")
    order = models.ForeignKey(
        OrderModel, on_delete=models.CASCADE, related_name="company_offer")
    description = models.TextField(max_length=2000)
    price = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if an offer already exists for the user and order combination
        existing_offer = OfferModel.objects.filter(
            user=self.user, order=self.order).first()

        if existing_offer:
            # If an offer already exists, raise an exception or handle the error as desired
            raise ValueError(
                "An offer already exists for this user and order.")

        super().save(*args, **kwargs)


class OfferMessageModel(models.Model):
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(OfferModel, on_delete=models.PROTECT)
    description = models.TextField()
    is_seen = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_date"]

    def get_username(self):
        if self.user:
            if self.user.company_profile.name:
                return self.user.company_profile.name
            return self.user.username
        elif self.email:
            return self.email.split("@")[0]
        else:
            return "Anonymous"

    def get_user_type(self):
        if self.is_company:
            return "Company"
        return "User"


class OfferTemplateModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=2000)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_title(self):
        if (not self.title) or (len(self.title) < 1):
            return f"template - {self.id}"
        else:
            return self.title

    def brief_description(self):

        # remove spaces between tags
        value = strip_spaces_between_tags(self.description)

        # add space before each P end tag (</p>)
        value = value.replace("</p>", " </p>")
        value = value.replace("&quot", "  ")
        # strip HTML tags
        value = strip_tags(value)

        # other usage: return Truncator(value).words(length, html=True, truncate=' see more')
        return Truncator(value).words(20)


class AgreedOffer(models.Model):
    offer = models.ForeignKey(OfferModel, on_delete=models.CASCADE)

    is_canceled = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']


@receiver(post_save, sender=OfferModel)
def inform_user(sender, instance, created, **kwargs):
    if created:
        send_offer_notify_to_user(to_email=instance.order.email,
                                  order=instance.order,
                                  company_profile=instance.user.profile,
                                  offer=instance)
@receiver(post_save, sender=AgreedOffer)
def inform_user(sender, instance, created, **kwargs):
    if created:
        send_offer_accepted_to_company(to_email=instance.offer.order.email,
                                  order=instance.offer.order,
                                  company_profile=instance.offer.user.profile,
                                  offer=instance.offer)
    if instance.is_canceled:
        send_offer_canceled_to_company(to_email=instance.offer.order.email,
                                  order=instance.offer.order,
                                  company_profile=instance.offer.user.profile,
                                  offer=instance.offer)