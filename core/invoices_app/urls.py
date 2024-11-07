from django.urls import path, include, re_path
from invoices_app import views
app_name = "invoices"

urlpatterns = [
    # api for offers
    path("generate-invoice",views.GenerateInvoiceView.as_view(),name="generate-invoice")
]