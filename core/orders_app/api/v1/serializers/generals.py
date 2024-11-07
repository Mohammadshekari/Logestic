from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
import json
from orders_app.models import OrderOriginModel, OrderDestinationModel, OrderModel, MoveDate
from orders_app.utils import calculate_google_map_distance
from orders_app.api.v1.exceptions import CustomValidationException

class OrderOriginSerializer(serializers.ModelSerializer):
    location_point = serializers.CharField()

    class Meta:
        model = OrderOriginModel
        fields = [
            "location_type",
            "moving_choice",
            "street",
            "zip_code",
            "city",
            "floor",
            "has_elevator",
            "apartment_size",
            "location_point"
        ]

    def validate_location_point(self, value):
        try:
            geojson_point = json.loads(value)
            if geojson_point["type"] == "Point" and len(geojson_point["coordinates"]) == 2:
                return GEOSGeometry(json.dumps(geojson_point))
            raise CustomValidationException("Invalid GeoJSON format for location_point.")
        except (ValueError, KeyError, TypeError) as e:
            raise CustomValidationException(f"Invalid location_point data: {e}")


class OrderDestinationSerializer(serializers.ModelSerializer):
    location_point = serializers.CharField()

    class Meta:
        model = OrderDestinationModel
        fields = [
            "location_type",
            "street",
            "zip_code",
            "city",
            "floor",
            "has_elevator",
            "location_point"
        ]

    def validate_location_point(self, value):
        try:
            geojson_point = json.loads(value)
            if geojson_point["type"] == "Point" and len(geojson_point["coordinates"]) == 2:
                return GEOSGeometry(json.dumps(geojson_point))
            raise CustomValidationException("Invalid GeoJSON format for location_point.")
        except (ValueError, KeyError, TypeError) as e:
            raise CustomValidationException(f"Invalid location_point data: {e}")


class OrderSerializer(serializers.ModelSerializer):
    move_dates = serializers.CharField()

    class Meta:
        model = OrderModel
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "move_dates",
            "living_people",
            "description",
        ]

    def create(self, validated_data):
        move_dates_str = validated_data.pop("move_dates", "")
        order = super().create(validated_data)

        # Process move_dates
        dates_list = move_dates_str.split(",")
        order.move_dates.clear()

        for date_str in dates_list:
            move_obj, created = MoveDate.objects.get_or_create(
                date=date_str.strip()
            )
            order.move_dates.add(move_obj)
        
        return order

    def update(self, instance, validated_data):
        move_dates_str = validated_data.pop("move_dates", "")
        instance = super().update(instance, validated_data)

        # Process move_dates
        dates_list = move_dates_str.split(",")
        instance.move_dates.clear()

        for date_str in dates_list:
            move_obj, created = MoveDate.objects.get_or_create(
                date=date_str.strip()
            )
            instance.move_dates.add(move_obj)

        return instance


class GeneralCreateOrderSerializer(serializers.Serializer):
    order = OrderSerializer()
    destination = OrderDestinationSerializer()
    origin = OrderOriginSerializer()

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        origin_data = validated_data.pop('origin')
        destination_data = validated_data.pop('destination')

        order = OrderSerializer.create(OrderSerializer(), validated_data=order_data)
        origin = OrderOriginSerializer.create(OrderOriginSerializer(), validated_data=origin_data)
        destination = OrderDestinationSerializer.create(OrderDestinationSerializer(), validated_data=destination_data)

        # Link origin and destination to the order if required by your model logic
        order.origin = origin
        order.destination = destination
        order.save()
        calculate_google_map_distance(order)

        return {
            "order": order,
            "origin": origin,
            "destination": destination
        }
