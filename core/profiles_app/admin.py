from django.contrib import admin
from profiles_app.models import *
# Register your models here.


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name']


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name']
