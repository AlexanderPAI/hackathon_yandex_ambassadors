# Generated by Django 5.0.2 on 2024-03-06 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promo", "0003_alter_merchapplication_ambassador_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="merchapplication",
            name="ambassador",
        ),
        migrations.RemoveField(
            model_name="promocode",
            name="ambassador",
        ),
        migrations.AddField(
            model_name="merchapplication",
            name="promocode",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merch_applications",
                to="promo.promocode",
                verbose_name="Promocode",
            ),
        ),
    ]
