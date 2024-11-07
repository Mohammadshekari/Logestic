from django import forms
from profiles_app.models import CompanyProfile, CompanyServicesType, PaymentMethodsType


class AdminCompanyProfileForm(forms.ModelForm):
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
            "status"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom classes to fields
        self.fields['status'].widget.attrs['class'] = 'form-select'


    def save(self, commit=True):
        instance = super(AdminCompanyProfileForm, self).save(commit=False)

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


