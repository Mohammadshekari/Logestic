from django.urls import path, include
from .. import views


urlpatterns = [

    # invoices management urls
    path("invoice/list/", views.CompanyInvoiceListView.as_view(), name="invoice-list"),
    path("invoice/<int:pk>/detail/",
         views.CompanyInvoiceDetailView.as_view(), name="invoice-detail"),
]
