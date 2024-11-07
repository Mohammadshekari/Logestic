# Generated by Django 4.2.16 on 2024-11-01 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices_app", "0005_invoicemodel_month_invoicemodel_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoicemodel",
            name="final_amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="invoicemodel",
            name="total_tax_amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
