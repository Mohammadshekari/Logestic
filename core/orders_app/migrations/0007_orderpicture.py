# Generated by Django 4.2.5 on 2023-11-10 08:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "orders_app",
            "0006_movedate_remove_ordermodel_move_date_ordermodel_uuid_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderPicture",
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
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders_app.ordermodel",
                    ),
                ),
            ],
        ),
    ]