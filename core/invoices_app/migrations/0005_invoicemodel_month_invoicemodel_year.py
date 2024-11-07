# Generated by Django 4.2.15 on 2024-08-24 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices_app", "0004_invoicemodel_deadline_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoicemodel",
            name="month",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="invoicemodel",
            name="year",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]