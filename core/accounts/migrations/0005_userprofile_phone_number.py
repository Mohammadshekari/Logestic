# Generated by Django 4.2.5 on 2023-10-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "accounts",
            "0004_rename_profile_userprofile_remove_user_auth_provider_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]