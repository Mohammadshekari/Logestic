# Generated by Django 4.2.7 on 2024-01-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("invoices_app", "0003_rename_total_price_invoicemodel_total_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoicemodel",
            name="deadline_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]