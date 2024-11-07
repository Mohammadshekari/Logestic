from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from accounts.models import UserType
from django.core.validators import MaxValueValidator, MinValueValidator
from .emails import send_company_welcome
import json
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], blank=True, null=True,default="/default/company-avatar-default.png")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="admin_profile")
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], blank=True, null=True,default="/default/company-avatar-default.png")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class CompanyServicesType(models.IntegerChoices):
    standard = 1 , _("Wheelbarrow as standard equipment")
    assessment_visit = 2 , _("Assessment visit can be arranged")
    rent_box = 3 , _("Rental of moving box")
    piano_transport = 4 , _("Piano transport")
    pack_unpack = 5 , _("Packing and unpacking service")
    cleaning = 6 , _("Moving cleaning")
    

class PaymentMethodsType(models.IntegerChoices):
    cash = 1, _("cash")
    card = 2, _("card")
    fall = 3, _("fall")
    invoice = 4, _("invoice")
    installment = 5, _("installment")

class CompanyProfileStatusType(models.IntegerChoices):
    pending = 1, _("pending")
    verified = 2, _("verified")
    rejected = 3, _("rejected")
    suspended = 4, _("suspended")

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="company_profile")
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], blank=True, null=True,default="/default/company-avatar-default.png")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(null=True,blank=True)
    service_types = ArrayField(models.IntegerField(choices=CompanyServicesType.choices), default=list, blank=True, null=True)
    
    street = models.CharField(max_length=255,null=True,blank=True)
    zip_code = models.CharField(max_length=255,null=True,blank=True)
    
    payment_method_types = ArrayField(models.IntegerField(choices=PaymentMethodsType.choices), default=list, blank=True, null=True)
    payment_description = models.TextField(max_length=2000, blank=True, null=True)
    
    serial_number = models.CharField(max_length=20, blank=True, null=True,help_text="Y ID")
    established_date = models.DateField(null=True,blank=True)
    
    rate = models.FloatField(default=0, validators=[
                               MinValueValidator(0.0), MaxValueValidator(5.0)])
    
    location_point = models.PointField(null=True)
    
    traffic_permit_id = models.CharField(max_length=255,null=True)
    status = models.IntegerField(choices=CompanyProfileStatusType.choices,default=CompanyProfileStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    def get_status(self):
        return {
            "id":self.status,
            "title":CompanyProfileStatusType(self.status).name,
            "label":CompanyProfileStatusType(self.status).label
            
        }
    def get_latlng(self):
        try:
            return json.dumps({"lng": self.location_point.coords[1], "lat": self.location_point.coords[0]})
 
        except:
            return None
            
    

class CompanyProfileImage(models.Model):
    profile = models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.normal.value:
        UserProfile.objects.create(user=instance,pk=instance.pk)
    if created and instance.type == UserType.company.value:
        CompanyProfile.objects.create(user=instance,pk=instance.pk)
        send_company_welcome(to_email=instance.email,user=instance)
    if created and instance.type == UserType.admin.value:
        AdminProfile.objects.create(user=instance,pk=instance.pk)
