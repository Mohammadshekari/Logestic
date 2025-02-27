# Generated by Django 4.2.7 on 2023-12-30 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("offers_app", "0006_offermessagemodel_is_seen"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="offermessagemodel",
            options={"ordering": ["created_date"]},
        ),
        migrations.AddField(
            model_name="offermessagemodel",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="offermessagemodel",
            name="is_processed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="offermessagemodel",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
