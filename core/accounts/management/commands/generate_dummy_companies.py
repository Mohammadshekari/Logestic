from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles_app.models import CompanyProfile,PaymentMethodsType,CompanyServicesType
import json
from faker import Faker
import random

User = get_user_model()

class Command(BaseCommand):
    help = "inserting dummy companies"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        self.generate_companies()

    def generate_companies(self):
        payment_types = [types[0] for types in PaymentMethodsType.choices]
        service_types = [types[0] for types in CompanyServicesType.choices]
        for _ in range(10):
            user_obj = User.objects.create_company(
                email = self.faker.email(),
                password = "a/@1234567"
            )
            company_profile = user_obj.company_profile
            company_profile.name = self.faker.company()
            company_profile.description = self.faker.paragraph()
            
            company_profile.phone_number = self.generate_random_finnish_phone_number()
            company_profile.email = user_obj.email
            company_profile.service_types = random.choices(service_types, k=2)
            company_profile.payment_method_types = random.choices(payment_types, k=2)
            company_profile.payment_description = self.faker.paragraph()
            company_profile.serial_number = self.faker.ssn()
            company_profile.established_date = self.faker.date()
            company_profile.save()
        print("finished creating 10 dummy companies")

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

    
