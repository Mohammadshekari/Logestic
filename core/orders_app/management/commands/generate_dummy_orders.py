from django.core.management.base import BaseCommand
import json
from orders_app.models import (OrderModel, OrderOriginModel,
                               OrderDestinationModel, LocationType, MovementType, MoveDate)
from faker import Faker
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "inserting dummy orders"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        self.generate_orders()

    def generate_orders(self):
        for _ in range(10):
            order_obj = OrderModel.objects.create(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                email=self.faker.email(),
                phone_number=self.generate_random_finnish_phone_number(),
                living_people=random.randint(0, 10),
                description=self.faker.paragraph(),
            )
            move_date_instances = []
            for date in self.generate_order_move_dates():
                move_date, _ = MoveDate.objects.get_or_create(date=date)
                move_date_instances.append(move_date)

            # Associate MoveDate instances with the OrderModel instance
            order_obj.move_dates.set(move_date_instances)

            OrderOriginModel.objects.create(
                order=order_obj,
                location_type=random.choice(
                    [item[0] for item in LocationType.choices]),
                moving_choice=random.choice(
                    [item[0] for item in MovementType.choices]),
                street=self.faker.street_address(),
                zip_code=self.faker.zipcode(),
                city=self.faker.city(),
                floor=random.randint(1, 20),
                has_elevator=random.choice([True, False]),
                apartment_size=random.randint(50, 100),
            )
            OrderDestinationModel.objects.create(
                order=order_obj,
                location_type=random.choice(
                    [item[0] for item in LocationType.choices]),
                street=self.faker.street_address(),
                zip_code=self.faker.zipcode(),
                city=self.faker.city(),
                floor=random.randint(1, 20),
                has_elevator=random.choice([True, False]),
            )
        print("finished creating 10 dummy orders")

    def generate_random_finnish_phone_number(self):
        # 0 = prefix (2), 1 = main digit, 2-5 = suffix
        digits = [random.randint(0, 9) for _ in range(6)]

        # Main digit should not be 0, 4 or 5
        while digits[1] in [0, 4, 5]:
            digits[1] = random.randint(1, 9)

        # Ensure prefix (2)
        digits[0] = 2

        # Formatting the number to fit Finnish phone number format
        return f"+358 {digits[0]}{digits[1]}{digits[2]}{digits[3]}{digits[4]}{digits[5]}"

    def generate_order_move_dates(self):
        move_dates = []
        current_date = datetime.today()
        thirty_day_delta = current_date + timedelta(days=30)
        for _ in range(random.randint(1,5)):
            move_dates.append(self.faker.date_between_dates(date_start=current_date, date_end=thirty_day_delta))
        return move_dates
