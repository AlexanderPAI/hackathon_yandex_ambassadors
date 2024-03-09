# Generated by Django 5.0.2 on 2024-03-08 07:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ambassadors", "0002_initial"),
        ("promo", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="merchapplication",
            name="tutor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merch_applications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AddField(
            model_name="merch",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merch",
                to="promo.merchcategory",
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="merchinapplication",
            name="application",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merch_in_applications",
                to="promo.merchapplication",
                verbose_name="Application",
            ),
        ),
        migrations.AddField(
            model_name="merchinapplication",
            name="merch",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merch_in_applications",
                to="promo.merch",
                verbose_name="Merch",
            ),
        ),
        migrations.AddField(
            model_name="merchapplication",
            name="merch",
            field=models.ManyToManyField(
                related_name="applications",
                through="promo.MerchInApplication",
                to="promo.merch",
                verbose_name="Merch",
            ),
        ),
        migrations.AddField(
            model_name="promocode",
            name="ambassador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="promocodes",
                to="ambassadors.ambassador",
                verbose_name="Ambassador",
            ),
        ),
        migrations.AddConstraint(
            model_name="merch",
            constraint=models.UniqueConstraint(
                fields=("name", "size"), name="name_size_unique_merch"
            ),
        ),
    ]