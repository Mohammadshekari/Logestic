# Generated by Django 4.2.7 on 2024-01-07 15:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("invoices_app", "0002_remove_invoicemodel_commission_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invoicemodel",
            old_name="total_price",
            new_name="total_amount",
        ),
    ]
