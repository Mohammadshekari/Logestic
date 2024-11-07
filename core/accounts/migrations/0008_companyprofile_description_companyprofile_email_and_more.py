# Generated by Django 4.2.5 on 2023-11-13 10:15

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_alter_companyprofile_user_alter_userprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyprofile",
            name="description",
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="founded_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="image",
            field=models.FileField(
                blank=True,
                default="",
                null=True,
                upload_to="",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png"]
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="payment_description",
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="payment_method_types",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(choices=[(1, "card"), (2, "cash")]),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="serial_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="companyprofile",
            name="service_types",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(
                    choices=[(1, "piano"), (2, "furniture")]
                ),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.CreateModel(
            name="CompanyProfileImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png"]
                            )
                        ],
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.companyprofile",
                    ),
                ),
            ],
        ),
    ]