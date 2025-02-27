# Generated by Django 4.2.7 on 2023-12-29 09:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "profiles_app",
            "0002_rename_founded_date_companyprofile_established_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyprofile",
            name="payment_method_types",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(
                    choices=[
                        (1, "cash"),
                        (2, "card"),
                        (3, "fall"),
                        (4, "invoice"),
                        (5, "installment"),
                    ]
                ),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="companyprofile",
            name="serial_number",
            field=models.CharField(
                blank=True, help_text="Y ID", max_length=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="companyprofile",
            name="service_types",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(
                    choices=[
                        (1, "Wheelbarrow as standard equipment"),
                        (2, "Assessment visit can be arranged"),
                        (3, "Rental of moving box"),
                        (4, "Piano transport"),
                        (5, "Packing and unpacking service"),
                        (6, "Moving cleaning"),
                    ]
                ),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="companyprofile",
            name="traffic_permit_id",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
