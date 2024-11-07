from django import forms
from orders_app.models import *
from django.core.exceptions import ValidationError


class OrderOriginForm(forms.ModelForm):
    location_point = forms.CharField()

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


class OrderDestinationForm(forms.ModelForm):
    location_point = forms.CharField()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['move_dates'].widget.attrs.update(
            {'id': 'datePicker','class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'summernote'})
        self.fields['living_people'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Save the OrderModel instance to get an id
        if commit:
            instance.save()


        move_dates = self.cleaned_data.get("move_dates", "")

        # Split move_dates string into individual dates
        dates_list = move_dates.split(",")

        # Clear existing move_dates
        instance.move_dates.clear()

        for date_str in dates_list:
            move_obj, created = MoveDate.objects.get_or_create(
                date=date_str.strip())
            instance.move_dates.add(move_obj)
        return instance


class AddOrderForm(forms.Form):
    order = OrderForm()
    destination = OrderDestinationForm(prefix="destination")
    origin = OrderOriginForm(prefix="origin")
    

