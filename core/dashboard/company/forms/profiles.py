from django import forms
from profiles_app.models import CompanyProfile, CompanyServicesType, PaymentMethodsType
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.gis.geos import GEOSGeometry
import json
from django.contrib.gis.geos import Point
class CompanyChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Invalid old password.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')

        return new_password2

class CompanyProfileForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        choices=CompanyServicesType.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    payments = forms.MultipleChoiceField(
        choices=PaymentMethodsType.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    traffic_permit_id = forms.CharField(required=False)
    location_point = forms.CharField()
    class Meta:
        model = CompanyProfile
        fields = [
            "name",
            "description",
            "phone_number",
            "email",
            "traffic_permit_id",
            "services",
            "payments",
            "payment_description",
            "serial_number",
            "established_date",
            "location_point"
        ]
    def clean_location_point(self):
        location_point = self.cleaned_data.get("location_point")
        if location_point:
            try:
                geojson_point = json.loads(location_point)
                # Ensure the geojson_point is a valid GeoJSON structure
                if geojson_point["type"] == "Point" and len(geojson_point["coordinates"]) == 2:
                    # Create GEOSGeometry object
                    point = GEOSGeometry(json.dumps(geojson_point))
                    return point
                else:
                    raise forms.ValidationError("Invalid GeoJSON format for location_point.")
            except (ValueError, KeyError, TypeError) as e:
                raise forms.ValidationError(f"Invalid location_point data: {e}")
        return None

    
    def save(self, commit=True):
        instance = super(CompanyProfileForm, self).save(commit=False)
        

        # Extract selected IDs from services and payments fields
        service_ids = [int(service_id)
                       for service_id in self.cleaned_data.get('services', [])]
        payment_ids = [int(payment_id)
                       for payment_id in self.cleaned_data.get('payments', [])]

        # Save the extracted IDs into the model fields
        instance.service_types = service_ids
        instance.payment_method_types = payment_ids

        if commit:
            instance.save()

        return instance


class CompanyProfileImageForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "image",
        ]
