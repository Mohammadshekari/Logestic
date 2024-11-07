from django.urls import path, include, re_path

app_name = "api"

urlpatterns = [
    path("generals/",include("orders_app.api.v1.urls.generals"))
    
    
]