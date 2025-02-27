# Generated by Django 4.2.5 on 2023-11-14 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders_app", "0008_ordermodel_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderdestinationmodel",
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_destination",
                to="orders_app.ordermodel",
            ),
        ),
        migrations.AlterField(
            model_name="orderoriginmodel",
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_origin",
                to="orders_app.ordermodel",
            ),
        ),
    ]
