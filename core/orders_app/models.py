from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth import get_user_model
import json
import uuid
from django.core.validators import FileExtensionValidator
from django.db.models import Count
from django.dispatch import receiver
from .emails import *
from django.db.models.signals import post_save
from orders_app.utils import ZipCodeConverter
from django.contrib.gis.measure import Distance, D


User = get_user_model()


class OrderStateType(models.IntegerChoices):
    pending = 1, "pending"
    in_process = 2, "in_process"
    done = 3, "done"
    canceled = 4, "canceled"


class LocationType(models.IntegerChoices):
    apartment = 1, "Apartment building"
    row_house = 2, "Row house"
    detached_house = 3, "Detached house"
    semi_detached_house = 4, "Semi-detached house"
    luhtitalo = 5, "Luhtitalo"
    storage = 6, "Storage space"
    company = 7, "Company relocation"
    other = 8, "Other"


class MovementType(models.IntegerChoices):
    all_items = 1, "all the items"
    only_a_part = 2, "only a part of the items"
    only_piano = 3, "only a piano move"

# Create your models here.


class MoveDate(models.Model):
    date = models.DateField()


class OrderModel(models.Model):
    BASE_PRICE = 5

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    move_dates = models.ManyToManyField(MoveDate)  # multiple time
    living_people = models.IntegerField(
        default=0)  # how many people live there
    description = models.TextField()

    state = models.IntegerField(
        choices=OrderStateType.choices, default=OrderStateType.pending.value)

    google_map_distance = models.FloatField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    price = models.DecimalField(decimal_places=2, max_digits=1000, default=5)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

    @property
    def offers_count(self):
        value = self.offers_count_cache if hasattr(
            self, 'offers_count_cache') else self.calculate_offers_count()
        return value

    def calculate_offers_count(self):
        self.offers_count_cache = self.company_offer.aggregate(count=Count('id'))[
            'count']
        return self.offers_count_cache

    def get_fullname(self):
        return self.first_name + " " + self.last_name

    def get_distance(self):
        try:
            distance = self.order_origin.location_point.distance(
                self.order_destination.location_point)
            return round(distance * 100, ndigits=2)
        except:
            return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderOriginModel(models.Model):
    order = models.OneToOneField(
        OrderModel, on_delete=models.CASCADE, related_name="order_origin")
    location_type = models.IntegerField(
        choices=LocationType.choices, default=LocationType.apartment.value)
    moving_choice = models.IntegerField(
        choices=MovementType.choices, default=MovementType.all_items.value)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    location_point = models.PointField(null=True, blank=True)
    city = models.CharField(max_length=255)
    floor = models.IntegerField(null=True, blank=True)
    has_elevator = models.BooleanField(default=False)
    apartment_size = models.IntegerField(null=True, blank=True)
        
    @property
    def address(self):
        return f"{self.city} - {self.street} - {self.zip_code} ..."

    def get_location_type(self):
        return LocationType(self.location_type).label

    def get_moving_choice(self):
        return MovementType(self.moving_choice).label

    def get_latlng(self):
        try:
            return json.dumps({"lng": self.location_point.coords[1], "lat": self.location_point.coords[0]})

        except:
            return None

    def get_movement_choice_price(self):
        if self.moving_choice == MovementType.all_items.value:
            return 5
        elif self.moving_choice == MovementType.only_piano.value:
            return 1
        elif self.moving_choice == MovementType.only_a_part.value:
            return 0
        else:
            return 0

    def get_apartment_size_price(self):
        return self.apartment_size % 10

    def recalculate_price(self):
        order_obj = self.order
        movement_price = self.get_movement_choice_price()
        apartment_area_price = self.get_apartment_size_price()

        order_obj.price = OrderModel.BASE_PRICE + movement_price + apartment_area_price
        order_obj.save()
        
    def save(self, *args, **kwargs):
        self.recalculate_price()
        super().save(*args, **kwargs)



class OrderDestinationModel(models.Model):
    order = models.OneToOneField(
        OrderModel, on_delete=models.CASCADE, related_name="order_destination")
    location_type = models.IntegerField(
        choices=LocationType.choices, default=LocationType.apartment.value)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    location_point = models.PointField(null=True, blank=True)
    city = models.CharField(max_length=255)
    floor = models.IntegerField(null=True, blank=True)
    has_elevator = models.BooleanField(default=False)

    def get_location_type(self):
        return LocationType(self.location_type).label

    def get_latlng(self):
        try:
            return json.dumps({"lng": self.location_point.coords[1], "lat": self.location_point.coords[0]})

        except:
            return None


class OrderPicture(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    file = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'])])

    def save(self, *args, **kwargs):

        if OrderPicture.objects.filter(order=self.order).count() >= 6:
            # If an offer already exists, raise an exception or handle the error as desired
            raise ValueError(
                "You have reached the maximum limit of images for each order")

        super().save(*args, **kwargs)


@receiver(post_save, sender=OrderDestinationModel)
def inform_user(sender, instance, created, **kwargs):
    if created:
        send_order_created_to_user(to_email=instance.order.email,
                                   order=instance.order)


# @receiver(post_save, sender=OrderDestinationModel)
# def convert_destination_zipcode(sender, instance, created, **kwargs):
#     try:
#         point = ZipCodeConverter.get_point(instance.zip_code)
#         geo_point = GEOSGeometry(json.dumps(point['geometry']))
#     except:
#         pass
#     else:
#         instance.geometry=geo_point
#         instance.save()


# @receiver(post_save, sender=OrderOriginModel)
# def convert_origin_zipcode(sender, instance, created, **kwargs):
#     try:
#         point = ZipCodeConverter.get_point(instance.zip_code)
#         geo_point = GEOSGeometry(json.dumps(point['geometry']))
#     except:
#         pass
#     else:
#         instance.geometry=geo_point
#         instance.save()

# @receiver(post_save, sender=OrderDestinationModel)
# def calculate_google_map_distance(sender, instance, created, **kwargs):
#     try:
#         instance = instance.order
#         origin = instance.order_origin.location_point.coords # Example: Colosseum in Rome
#         destination = instance.order_destination.location_point.coords # Example: Palermo in Sicily

#         # Request directions
#         directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())

#         # Extract distance from the directions result
#         if directions_result and 'legs' in directions_result[0]:
#             distance_meters = directions_result[0]['legs'][0]['distance']['value']
#             distance = distance_meters / 1000
#             instance.google_map_distance = distance
#             instance.save()
#     except:
#         raise
