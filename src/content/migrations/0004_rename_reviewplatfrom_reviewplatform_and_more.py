# Generated by Django 5.0.2 on 2024-03-09 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0003_alter_reviewplatfrom_slug"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ReviewPlatfrom",
            new_name="ReviewPlatform",
        ),
        migrations.DeleteModel(
            name="GuideStatus",
        ),
        migrations.AlterField(
            model_name="contentplatform",
            name="slug",
            field=models.SlugField(
                blank=True, null=True, unique=True, verbose_name="slug"
            ),
        ),
    ]
