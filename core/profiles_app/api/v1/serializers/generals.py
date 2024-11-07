from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles_app.models import CompanyProfile

User = get_user_model()

class GeneralAddCompanySerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    serial_number = serializers.CharField()

    def validate_email(self, value):
        # Check if a user with the provided email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_name(self, value):
        # Add any custom validation for name
        return value

    def validate_phone_number(self, value):
        # Add any custom validation for phone_number
        return value

    def validate_serial_number(self, value):
        # Add any custom validation for serial_number
        return value

    def create(self, validated_data):
        # Extract validated data
        email = validated_data.get("email")
        name = validated_data.get("name")
        phone_number = validated_data.get("phone_number")
        serial_number = validated_data.get("serial_number")

        # Create a new user with a random password
        password = "a/@1234567"
        user = User.objects.create_company(email=email, password=password)

        # Create or update the associated CompanyProfile
        company_profile = user.profile
        company_profile.name = name
        company_profile.phone_number = phone_number
        company_profile.serial_number = serial_number
        company_profile.save()

        return user
