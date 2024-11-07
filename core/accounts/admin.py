from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ("email",)
    list_filter = ("email", "is_active", "is_staff","type")
    ordering = ("-created_date",)
    list_display = ("id","email","type" ,"is_active", "is_staff","is_verified")
    fieldsets = (
        ("Authentication", {"fields": ("email","password")}),
        ("User information", {"fields": ("type",)}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_verified")}),
        (
            "Group Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "type",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_verified"
                ),
            },
        ),
    )
    

admin.site.register(User, UserAdminConfig)
