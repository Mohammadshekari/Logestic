from django import forms
from tickets_app.models import *


class TicketCompanyForm(forms.ModelForm):

    class Meta:
        model = TicketModel
        fields = [
            "priority",
            "title",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom classes to fields
        self.fields['priority'].widget.attrs['class'] = 'form-select'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


class TicketMessageForm(forms.ModelForm):

    class Meta:
        model = TicketMessageModel
        fields = [
            "description",
        ]
