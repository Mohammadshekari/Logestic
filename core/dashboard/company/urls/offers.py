from django.urls import path, include
from .. import views


urlpatterns = [

    # offers management urls
    path("offer/list/", views.CompanyOfferListView.as_view(), name="offer-list"),
    path("offer/<int:pk>/detail/",
         views.CompanyOfferDetailView.as_view(), name="offer-detail"),
    path("offer/<int:pk>/send-message/",
         views.CompanyOfferSendMessageView.as_view(), name="offer-send-message"),
]
