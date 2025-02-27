# Generated by Django 4.2.5 on 2023-11-15 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders_app", "0009_alter_orderdestinationmodel_order_and_more"),
        ("offers_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offermodel",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_offer",
                to="orders_app.ordermodel",
            ),
        ),
    ]
