from rest_framework import viewsets, generics, mixins, views
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from notifier_app.models import *
from notifier_app.api.v1.serializers import *
from notifier_app.api.paginations import *
from notifier_app.api.v1.exceptions import CustomValidationException

class NotificationListApiView(generics.ListAPIView):
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_date','is_read']
    pagination_class = DefaultPagination

    def get_queryset(self):
        return NotificationModel.objects.filter(user_id= self.request.user)


class NotificationListUnreadApiView(generics.ListAPIView):
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return NotificationModel.objects.filter(user_id= self.request.user,is_read=False)

class NotificationMarkAsReadApiView(generics.GenericAPIView):
    serializer_class = NotificationsMarkAsReadSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification_obj = serializer.validated_data['notification_obj']
        if notification_obj.is_read:
            return CustomValidationException({'detail':f'notification {notification_obj.id} has already marked as read'})
        notification_obj.is_read = True
        notification_obj.save()
        return Response({'detail':f'notification {notification_obj.id} marked as read'},status=status.HTTP_200_OK)

class NotificationMarkAsReadAllApiView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        notifications_query = NotificationModel.objects.filter(user_id=request.user,is_read=False)
        if notifications_query.exists():
            notifications_query.update(is_read=True)
        return Response({'detail':f'{notifications_query.count()} notifications marked as read'},status=status.HTTP_200_OK)