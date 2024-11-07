from django.conf import settings


# Custom User Management
LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL", "/")
ENABLE_ACCOUNTS_API = getattr(settings,"ENABLE_ACCOUNTS_API",False)
ENABLE_ACCOUNTS_PAGES = getattr(settings,"ENABLE_ACCOUNTS_PAGES",True)
# AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL","accounts.User")
# AUTH_PROFILE_MODULE = getattr(settings, "AUTH_PROFILE_MODULE","accounts.User")