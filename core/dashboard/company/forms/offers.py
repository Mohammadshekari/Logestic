from django import forms
from offers_app.models import *

class OfferMessageForm(forms.ModelForm):

    class Meta:
        model = OfferMessageModel
        fields = [
            "description",
        ]

