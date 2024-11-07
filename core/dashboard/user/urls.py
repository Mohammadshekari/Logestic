from django.urls import path, include
from . import views


app_name = 'user'

urlpatterns = [
    
    # order urls
    path("order/<uuid:uuid>/",views.OrderDetailView.as_view(),name="order-detail"),
    path("order/<uuid:uuid>/edit/",views.OrderEditView.as_view(),name="order-edit"),
    path("order/<uuid:uuid>/edit/basic-info/",views.OrderBasicInfoEditView.as_view(),name="order-edit-basic-info"),
    path("order/<uuid:uuid>/edit/origin-detail/",views.OrderOriginDetailEditView.as_view(),name="order-edit-origin-detail"),
    path("order/<uuid:uuid>/edit/destination-detail/",views.OrderDestinationDetailEditView.as_view(),name="order-edit-destination-detail"),
    path("order/<uuid:uuid>/close/",views.OrderCloseView.as_view(),name="order-close"),
    path("order/<uuid:uuid>/offer/<int:offer_id>/review",views.OrderOffersReviewView.as_view(),name="order-offers-review"),
    
    
    # order images
    path("order/<uuid:uuid>/pictures/",views.OrderPicturesView.as_view(),name="order-pictures"),
    path("order/<uuid:uuid>/pictures/<int:picture_id>/delete/",views.OrderPicturesDeleteView.as_view(),name="order-pictures-delete"),
    
    # offer urls
    path("order/<uuid:uuid>/offer/list/",views.OrderOffersListView.as_view(),name="order-offers-list"),
    path("order/<uuid:uuid>/offer/<int:offer_id>/",views.OrderOffersDetailView.as_view(),name="order-offers-detail"),
    path("order/<uuid:uuid>/offer/<int:offer_id>/accept/",views.OrderOffersAcceptView.as_view(),name="order-offers-accept"),
    path("order/<uuid:uuid>/offer/<int:offer_id>/cancel/",views.OrderOffersCancelView.as_view(),name="order-offers-cancel"),
    
    
    # company detail
    path("company/<int:pk>/profile/preview/",views.CompanyPreviewView.as_view(),name="company-profile-preview"),
    
    # conversations
    path("order/<uuid:uuid>/offer/<int:offer_id>/send-message/",views.UserOfferSendMessageView.as_view(),name="offer-send-message"),
    
    
]
