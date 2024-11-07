from django.core.management.base import BaseCommand
from offers_app.models import OfferTemplateModel
from profiles_app.models import CompanyProfile
from faker import Faker
import random


class Command(BaseCommand):
    help = "inserting dummy offer tempaltes"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        self.generate_offer_templates()

    def generate_offer_templates(self):
        company_profiles = CompanyProfile.objects.all()
        for profile in company_profiles:
            for _ in range(random.randint(1,5)):
                OfferTemplateModel.objects.create(
                    user =profile.user,
                    title = random.choice([None,"",self.generate_title()]),
                    description=" ".join(self.faker.paragraphs(nb=8))
                    )
        print("finished creating dummy offer templates")

    def generate_title(self):
        return self.faker.name()
    
