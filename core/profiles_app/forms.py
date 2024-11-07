from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from profiles_app.models import CompanyProfile
User = get_user_model()

class AddCompanyForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    phone_number = forms.CharField()
    serial_number = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom classes to fields
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['serial_number'].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')

        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Your custom name validation logic
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Your custom phone_number validation logic
        return phone_number

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        # Your custom serial_number validation logic
        return serial_number

    def clean(self):
        cleaned_data = super().clean()

        # Additional overall form validation logic if needed

        return cleaned_data

    def save(self):
        # Get data from the form
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        phone_number = self.cleaned_data.get('phone_number')
        serial_number = self.cleaned_data.get('serial_number')

        # Create a new user with a random password
        password = "a/@1234567"
        user = User.objects.create_company(email=email, password=password)
        
        company_profile = user.profile
        # Get or create the CompanyProfile based on the user
        # Update the CompanyProfile fields
        company_profile.name = name
        company_profile.phone_number = phone_number
        company_profile.serial_number = serial_number
        company_profile.save()
        return user