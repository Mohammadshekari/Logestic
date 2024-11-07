# Generated by Django 4.2.5 on 2023-10-02 19:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="type",
            field=models.IntegerField(
                choices=[(1, "normal"), (2, "company"), (3, "support"), (4, "admin")],
                default=1,
            ),
        ),
    ]