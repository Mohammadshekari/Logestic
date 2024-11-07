from django.contrib import admin
from orders_app.models import OrderModel, OrderDestinationModel, OrderOriginModel,MoveDate


# Register your models here.
@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id','uuid', 'email','phone_number', 'first_name', 'last_name']


@admin.register(OrderOriginModel)
class OrderOriginModelAdmin(admin.ModelAdmin):
    list_display = ['id','order', 'location_type',
                    'moving_choice', 'floor', 'zip_code', 'city']


@admin.register(OrderDestinationModel)
class OrderDestinationModelAdmin(admin.ModelAdmin):
    list_display = ['id','order', 'location_type', 'floor', 'zip_code', 'city']
@admin.register(MoveDate)
class MoveDateAdmin(admin.ModelAdmin):
    list_display = ['id','date']
