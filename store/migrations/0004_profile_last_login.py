# Generated by Django 4.2.13 on 2024-07-12 21:19

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_login",
            field=models.DateTimeField(
                auto_now=True, verbose_name=django.contrib.auth.models.User
            ),
        ),
    ]
