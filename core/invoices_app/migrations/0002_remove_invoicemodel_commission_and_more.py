# Generated by Django 4.2.7 on 2024-01-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("invoices_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoicemodel",
            name="commission",
        ),
        migrations.AddField(
            model_name="invoicemodel",
            name="total_price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]