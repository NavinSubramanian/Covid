# Generated by Django 5.0.1 on 2024-01-09 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_slot_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slot",
            name="name",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.center",
            ),
        ),
    ]