from django.urls import path, include, re_path
from orders_app.api.v1 import views

urlpatterns = [
      path(
        "create-order",
        views.CreateOrderModelViewSet.as_view(
            {"post": "create",}),
        name="create-order",
    ),
    
]