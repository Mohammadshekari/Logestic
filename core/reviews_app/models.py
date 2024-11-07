from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
# Create your models here.


class ReviewModel(models.Model):
    email = models.EmailField(null=True, blank=True)
    company = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT, null=True, blank=True,related_name="company_review_user")
    user = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT, null=True, blank=True,related_name="user_review_user")
    rate = models.IntegerField(default=5, validators=[
                               MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



@receiver(post_save, sender=ReviewModel)
def recalculate_review_rate(sender, instance, created, **kwargs):
       if created:
        # Calculate the average rating for the associated company
        company = instance.company
        average_rating = ReviewModel.objects.filter(company=company).aggregate(Avg('rate'))['rate__avg']

        # Update the company's rate attribute
        profile = company.company_profile
        profile.rate = round(average_rating, 2) if average_rating is not None else 0
        profile.save()