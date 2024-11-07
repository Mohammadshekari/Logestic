from django.contrib import admin
from reviews_app.models import *
# Register your models here.

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','company',"rate","created_date"]
