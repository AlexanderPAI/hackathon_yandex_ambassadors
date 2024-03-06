# Generated by Django 5.0.2 on 2024-03-04 07:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ambassadors", "0001_initial"),
        ("promo", "0003_alter_merchapplication_ambassador_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="ambassador",
            name="promocode",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to="promo.promocode",
            ),
        ),
        migrations.AlterField(
            model_name="ambassador",
            name="tutor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="ambassadormerch",
            name="merch",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to="promo.merch",
            ),
        ),
    ]