# Generated by Django 5.0.2 on 2024-03-08 07:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ambassadors", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="ambassador",
            name="tutor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Наставник",
            ),
        ),
        migrations.AddField(
            model_name="ambassadoractivity",
            name="activity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ambassadors.activity"
            ),
        ),
        migrations.AddField(
            model_name="ambassadoractivity",
            name="ambassador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ambassadors.ambassador"
            ),
        ),
        migrations.AddField(
            model_name="ambassador",
            name="activity",
            field=models.ManyToManyField(
                related_name="ambassadors",
                through="ambassadors.AmbassadorActivity",
                to="ambassadors.activity",
                verbose_name="Цель Амбассадорства",
            ),
        ),
        migrations.AddField(
            model_name="ambassador",
            name="program",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to="ambassadors.program",
                verbose_name="Программа в Практикуме",
            ),
        ),
        migrations.AddField(
            model_name="ambassador",
            name="purpose",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to="ambassadors.purpose",
                verbose_name="Цель в Практикуме",
            ),
        ),
        migrations.AddField(
            model_name="ambassador",
            name="status",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ambassadors",
                to="ambassadors.status",
                verbose_name="Статус",
            ),
        ),
    ]
