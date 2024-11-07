from django.urls import path, include
from .. import views

urlpatterns = [


    # orders management urls
    path("order/list/", views.CompanyOrderListView.as_view(), name="order-list"),
    path("order/<int:pk>/detail/",
         views.CompanyOrderDetailView.as_view(), name="order-detail"),
    path("order/<int:pk>/create-offer/",
         views.CompanyOrderCreateOfferView.as_view(), name="order-create-offer"),
]
