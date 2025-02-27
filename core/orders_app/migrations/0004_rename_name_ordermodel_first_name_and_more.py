# Generated by Django 4.2.5 on 2023-10-22 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders_app", "0003_ordermodel_created_date_ordermodel_updated_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ordermodel",
            old_name="name",
            new_name="first_name",
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
