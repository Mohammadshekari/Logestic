from django.urls import path, include
from .. import views

urlpatterns = [
    
    # offer templates management urls
    path("offer-template/list/", views.CompanyOfferTemplateListView.as_view(), name="offer-template-list"),
    path("offer-template/create/", views.CompanyOfferTemplateCreateView.as_view(), name="offer-template-create"),
    path("offer-template/<int:pk>/edit/", views.CompanyOfferTemplateEditView.as_view(), name="offer-template-edit"),
    path("offer-template/<int:pk>/delete/", views.CompanyOfferTemplateDeleteView.as_view(), name="offer-template-delete"),
    path("offer-template/<int:pk>/detail/json", views.CompanyOfferTemplateDetailJsonView.as_view(), name="offer-template-detail-json"),
]
