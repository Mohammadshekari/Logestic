from django import forms
from offers_app.models import *
from orders_app.models import *
from django.core.exceptions import ValidationError
class OfferMessageForm(forms.ModelForm):

    class Meta:
        model = OfferMessageModel
        fields = [
            "description",
        ]


class OrderForm(forms.ModelForm):
    move_dates = forms.CharField()
    class Meta:
        model = OrderModel
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "move_dates",
            "living_people",
            "description",
        ]
    def save(self, commit=True):
        instance = super().save(commit=False)
        move_dates = self.cleaned_data.get("move_dates", "")

        # Split move_dates string into individual dates
        dates_list = move_dates.split(",")
        
        # Clear existing move_dates
        instance.move_dates.clear()
        
        for date_str in dates_list:
            move_obj , created = MoveDate.objects.get_or_create(date=date_str.strip())
            instance.move_dates.add(move_obj)


        if commit:
            instance.save()

        return instance


class OrderOriginForm(forms.ModelForm):
    location_point = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'id_origin-location_point'})
    )
    class Meta:
        model = OrderOriginModel
        fields = [
            "location_type",
            "moving_choice",
            "street",
            "zip_code",
            "city",
            "floor",
            "has_elevator",
            "apartment_size",
            "location_point"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moving_choice'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['location_type'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['street'].widget.attrs.update({'class': 'form-control'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['floor'].widget.attrs.update({'class': 'form-control'})
        self.fields['has_elevator'].widget.attrs.update(
            {'class': 'form-check-input'})
        self.fields['apartment_size'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['location_point'].widget.attrs.update(
            {'class': 'form-control'})


class OrderDestinationForm(forms.ModelForm):
    location_point = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'id_destination-location_point'})
    )
    class Meta:
        model = OrderDestinationModel
        fields = [
            "location_type",
            "street",
            "zip_code",
            "city",
            "floor",
            "has_elevator",
            "location_point"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location_type'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['street'].widget.attrs.update({'class': 'form-control'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['floor'].widget.attrs.update({'class': 'form-control'})
        self.fields['has_elevator'].widget.attrs.update(
            {'class': 'form-check-input'})


class OrderPictureForm(forms.ModelForm):
    class Meta:
        model = OrderPicture
        fields = [
            "file",
        ]


