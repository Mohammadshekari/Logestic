from invoices_app.models import InvoiceModel
from django import forms


class InvoiceStateForm(forms.ModelForm):
    class Meta:
        model = InvoiceModel
        fields = [
            "state"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].widget.attrs.update(
            {'class': 'form-select'})
