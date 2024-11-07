from django.http import HttpResponse
from django.views import View
from invoices_app.tasks import generate_invoices

class GenerateInvoiceView(View):
    def get(self, request, *args, **kwargs):
        # Here you can add your logic for generating an invoice
        # For demonstration purposes, let's assume you generate a simple text response
        generate_invoices()
        

        return HttpResponse("")
