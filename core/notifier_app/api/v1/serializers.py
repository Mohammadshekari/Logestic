from django.core.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField
from rest_framework import permissions, serializers, status
from django.urls import reverse
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from notifier_app.models import NotificationModel
from notifier_app.api.v1.exceptions import CustomValidationException

class NotificationsSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = NotificationModel
        fields = [
            'id',
            "title",
            "content",
            'is_read',
            'created_date',

        ]
    
        

class NotificationsMarkAsReadSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField(required=True)
    
    def validate(self, attrs):
        try:
            attrs['notification_obj'] = NotificationModel.objects.get(id=attrs.get('notification_id',None),user_id= self.context['request'].user)
        except NotificationModel.DoesNotExist:
            raise CustomValidationException({"detail":"notification doesnt exists"})
        return super().validate(attrs)