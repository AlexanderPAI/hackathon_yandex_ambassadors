# Generated by Django 5.0.2 on 2024-03-09 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guidekit",
            name="tasks",
            field=models.ManyToManyField(
                blank=True,
                related_name="guide_kits",
                through="content.GuideTaskGuideKit",
                to="content.guidetask",
                verbose_name="Таски в наборе",
            ),
        ),
        migrations.AlterField(
            model_name="guidetask",
            name="type",
            field=models.CharField(
                choices=[
                    ("Photo", "Фотография в мерче"),
                    ("Review", "Отзыв"),
                    ("Content", "Контент"),
                ],
                max_length=200,
                verbose_name="Тип таски",
            ),
        ),
        migrations.AlterField(
            model_name="guidetaskguidekit",
            name="guide_kit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="connected_tasks",
                to="content.guidekit",
            ),
        ),
        migrations.AlterField(
            model_name="guidetaskguidekit",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="connected_tasks",
                to="content.guidetask",
            ),
        ),
    ]
