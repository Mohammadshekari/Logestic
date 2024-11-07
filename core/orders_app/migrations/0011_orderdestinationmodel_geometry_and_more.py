# Generated by Django 4.2.13 on 2024-07-10 02:28

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders_app", "0010_ordermodel_is_done"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderdestinationmodel",
            name="geometry",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326
            ),
        ),
        migrations.AddField(
            model_name="orderoriginmodel",
            name="geometry",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326
            ),
        ),
    ]