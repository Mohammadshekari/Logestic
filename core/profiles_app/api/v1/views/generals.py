from rest_framework.response import Response
from rest_framework import status, viewsets, views
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import action

from profiles_app.api.v1.serializers import *
from profiles_app.models import *
from profiles_app.api.v1.exceptions import CustomValidationException
from rest_framework.permissions import IsAuthenticated


from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action



class CreateCompanyProfileModelViewSet( viewsets.GenericViewSet):
    serializer_class = GeneralAddCompanySerializer

    def create(self, request, *args, **kwargs):
        # Instantiate the serializer with request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "detail":"created company profile successfully, check your email for further instructions."
        }
        return Response(response, status=status.HTTP_201_CREATED)