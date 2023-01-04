# Generated by Django 4.1.5 on 2023-01-04 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("custom_games", "0003_alter_customgames_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customgames",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="games",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]