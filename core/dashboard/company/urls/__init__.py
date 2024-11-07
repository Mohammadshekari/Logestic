from django.urls import path, include



app_name = 'company'

urlpatterns = [
    path("",include("dashboard.company.urls.generals")),
    path("",include("dashboard.company.urls.profiles")),
    path("",include("dashboard.company.urls.offer_templates")),
    path("",include("dashboard.company.urls.offers")),
    path("",include("dashboard.company.urls.orders")),
    path("",include("dashboard.company.urls.tickets")),
    path("",include("dashboard.company.urls.conversations")),
    path("",include("dashboard.company.urls.invoices")),
    
]
