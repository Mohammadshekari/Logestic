from django.core.management.base import BaseCommand
import json
from orders_app.models import OrderModel
from offers_app.models import OfferModel
from profiles_app.models import CompanyProfile
from faker import Faker
import random


class Command(BaseCommand):
    help = "inserting dummy offers"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        self.generate_offers()

    def generate_offers(self):
        orders_query = OrderModel.objects.all()
        company_profiles = CompanyProfile.objects.all()
        try:
            for company in company_profiles:            
                for order in orders_query:
                    OfferModel.objects.create(
                        order = order,
                        user = company.user,
                        description = self.faker.paragraph(nb_sentences=5, variable_nb_sentences=False)
                    )
        except:
            pass
        print("finished creating dummy offers")

    
