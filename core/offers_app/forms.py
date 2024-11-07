from django import forms
from offers_app.models import OfferModel,OfferTemplateModel



class OfferTemplateForm(forms.ModelForm):
     
    class Meta:
        model = OfferTemplateModel
        fields = ["title", "description"]



class OfferForm(forms.ModelForm):    
    class Meta:
        model = OfferModel
        fields = ["description","price"]
