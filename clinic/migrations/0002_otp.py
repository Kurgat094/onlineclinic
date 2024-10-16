# Generated by Django 5.1.1 on 2024-10-13 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Otp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("otp", models.CharField(max_length=6)),
                ("is_verified", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="clinic.users"
                    ),
                ),
            ],
        ),
    ]
