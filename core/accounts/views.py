from typing import Any
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.views import generic
from django.views.generic import base
from django.contrib.auth import views
from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .forms import UserSignUpForm, CompanySignUpForm, LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()

class RegistrationView(generic.TemplateView):
    template_name = 'accounts/register.html'


class RegistrationUserView(generic.CreateView):
    form_class = UserSignUpForm
    redirect_authenticated_user = True
    http_method_names = ['post']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. You can now log in.')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
        return redirect('accounts:register')

    def get_success_url(self):
        return reverse('accounts:login')


class RegistrationCompanyView(generic.CreateView):
    form_class = CompanySignUpForm
    redirect_authenticated_user = True
    http_method_names = ['post']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. You can now log in.')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
        return redirect('accounts:register')

    def get_success_url(self):
        return reverse('accounts:login')


class LoginView(SuccessMessageMixin, views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_message = "You have been successfully logged in!"

class LoginUseTokenView(View):
    def get(self, request, *args, **kwargs):
        authentication_key = request.GET.get('authentication_key')
        next = request.GET.get('next',None)

        if authentication_key:
            user_id = self.decode_jwt_token(authentication_key)
            if user_id:
                # Authenticate the user based on the user_id
                # Replace the following line with your authentication logic
                user = self.authenticate_user(user_id)
                if user:
                    # Redirect to a page after successful login
                    if next:
                        return redirect(next)
                    return redirect(reverse_lazy("dashboard:company:home"))
                else:
                    # Handle authentication failure
                    return HttpResponse('Authentication failed', status=401)
            else:
                # Handle invalid token
                return HttpResponse('Invalid token', status=400)
        else:
            # Handle missing authentication_key parameter
            return HttpResponse('Missing authentication_key parameter', status=400)

    def decode_jwt_token(self,token):
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_payload['user_id']
            # Return the user ID
            return user_id
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.DecodeError:
            # Handle invalid token
            return None

    def authenticate_user(self,user_id):
        user = User.objects.get(id=user_id)
        # user = authenticate(request=self.request,email=user.email)
        if user.is_active:
            login(self.request, user)
            return user
        else:
            return None

# class LogoutView(views.LogoutView):
#     template_name = 'accounts/logged_out.html'
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('accounts:login'))


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/emails/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
