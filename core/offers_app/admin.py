from django.contrib import admin
from offers_app.models import *
# Register your models here.


@admin.register(OfferModel)
class OfferModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'created_date']


@admin.register(OfferTemplateModel)
class OfferTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(AgreedOffer)
class AgreedOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'offer']


@admin.register(OfferMessageModel)
class OfferMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'offer']
