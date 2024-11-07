from django.urls import path, include, re_path
from . import views
app_name = "orders"

urlpatterns = [
    # api for orders
    path("api/v1/", include("orders_app.api.v1.urls")),
    
    # add orders tests
    path("add-order/",views.AddOrderView.as_view(),name="add-order"),
    path("add-order/completed/",views.AddOrderCompletedView.as_view(),name="add-order-completed")
]
