from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        super(UserSignUpForm, self).__init__(*args, **kwargs)

    def save(self):
        user_obj = User.objects.create_user(email=self.cleaned_data["email"],
                                            password=self.cleaned_data["password1"])
        return user_obj


class CompanySignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        super(CompanySignUpForm, self).__init__(*args, **kwargs)

    def save(self):
        user_obj = User.objects.create_company(email=self.cleaned_data["email"],
                                               password=self.cleaned_data["password1"])
        return user_obj


class LoginForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(LoginForm, self).confirm_login_allowed(user)

        # if not user.is_verified:
        #     raise ValidationError(
        #         "User is not verified yet, please follow the instructions for verification",
        #         code='not verified',
        #     )
        if user.is_superuser:
            raise ValidationError(
                "User is not verified yet, please follow the instructions for verification",
                code='not verified',
            )
