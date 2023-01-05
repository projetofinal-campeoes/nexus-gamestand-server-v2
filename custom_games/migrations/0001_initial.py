# Generated by Django 4.1.5 on 2023-01-05 17:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomGames",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=23)),
                ("image_url", models.TextField()),
                ("platform", models.CharField(max_length=16)),
            ],
        ),
    ]
