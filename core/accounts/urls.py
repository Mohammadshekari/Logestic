from django.urls import path, include
from . import views
from .app_settings import ENABLE_ACCOUNTS_API, ENABLE_ACCOUNTS_PAGES

app_name = "accounts"


urlpatterns = []


if ENABLE_ACCOUNTS_PAGES:
    urlpatterns += [

        # Base urls for authentication
        path('register/', views.RegistrationView.as_view(), name='register'),
        #    path('register/user/', views.RegistrationUserView.as_view(),
        #         name='register-user'),
        #    path('register/company/', views.RegistrationCompanyView.as_view(),
        #         name='register-company'),

        path('login/', views.LoginView.as_view(), name='login'),
        path('login/use-token/', views.LoginUseTokenView.as_view(),
             name='login-use-token'),
        path('logout/', views.LogoutView.as_view(), name='logout'),

        # password management
        #    path('password-change/', views.PasswordChangeView.as_view(),
        #         name='password_change'),
        #    path('password-change/done/', views.PasswordChangeDoneView.as_view(),
        #         name='password_change_done'),
        path('password-reset/', views.PasswordResetView.as_view(),
             name='password_reset'),
        path('password-reset/done/', views.PasswordResetDoneView.as_view(),
             name='password_reset_done'),
        path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
             name='password_reset_confirm'),
        path('reset/done/', views.PasswordResetCompleteView.as_view(),
             name='password_reset_complete'),
    ]


if ENABLE_ACCOUNTS_API:
    urlpatterns += [
        # api based authentication
        path("api/v1/", include("accounts.api.v1.urls"))
    ]
