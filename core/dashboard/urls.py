from django.urls import path, include
from . import views


app_name = "dashboard"


urlpatterns = [
    # access dashboard
    path("home/",views.DashboardHomeView.as_view(),name="home"),
    
    # admin dashboard management
    path('admin/',include('dashboard.admin.urls')),
    
    # company dashboard management
    path('company/',include('dashboard.company.urls')),
    
    # user order management
    path('user/',include('dashboard.user.urls')),
]
