from django.urls import path, include

app_name = 'admin'

urlpatterns = [
    path("",include("dashboard.admin.urls.generals")),
    path("",include("dashboard.admin.urls.profiles")),
    path("",include("dashboard.admin.urls.companies")),
    path("",include("dashboard.admin.urls.tickets")),
    path("",include("dashboard.admin.urls.invoices")),

]
