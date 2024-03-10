from django.db import models

from ambassadors.models import Ambassador


class GuideTask(models.Model):
    """Модель такси для гайда."""

    GUIDE_TASK_TYPE = {
        "Photo": "Фотография в мерче",
        "Review": "Отзыв",
        "Content": "Контент",
    }
    type = models.CharField(
        max_length=200,
        verbose_name="Тип таски",
        choices=GUIDE_TASK_TYPE,
    )

    class Meta:
        verbose_name = "Задача для гайда"
        verbose_name_plural = "Задачи для гайдов"
        ordering = ["id"]

    def __str__(self):
        return self.type


class GuideKit(models.Model):
    """Модель набора тасок."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название набора тасок",
    )
    tasks = models.ManyToManyField(
        GuideTask,
        through="GuideTaskGuideKit",
        through_fields=("guide_kit", "task"),
        related_name="guide_kits",
        blank=True,
        verbose_name="Таски в наборе",
    )

    class Meta:
        verbose_name = "Набор задач для гайда"
        verbose_name_plural = "Наборы задач для гайдов"
        ordering = ["name"]

    def __str__(self):
        return self.name


class GuideTaskGuideKit(models.Model):
    """Вспомогательная модель для M2M."""

    guide_kit = models.ForeignKey(
        GuideKit, on_delete=models.CASCADE, related_name="connected_tasks"
    )
    task = models.ForeignKey(
        GuideTask, on_delete=models.CASCADE, related_name="connected_tasks"
    )


class Guide(models.Model):
    STATUS = {
        "pause": "На паузе",
        "not_started": "Не приступил к прохождению",
        "started": "В процессе прохождения",
        "complete": "Завершен",
    }
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name="guides",
        verbose_name="Амбассадор",
    )
    guide_kit = models.ForeignKey(
        GuideKit,
        on_delete=models.CASCADE,
        related_name="guides",
        verbose_name="Набор тасок",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS,
        blank=True,
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Гайд"
        verbose_name_plural = "Гайды"
        ordering = ["ambassador"]

    def __str__(self):
        return f"Гайд {self.ambassador.name}"


class MerchPhoto(models.Model):
    """Модель фото амбассадора в мерче."""

    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name="merch_photos",
        verbose_name="Амбассадор",
    )
    photo = models.ImageField(
        upload_to="content/", blank=True, verbose_name="Фото в мерче"
    )

    class Meta:
        verbose_name = "Фотография в мерче"
        verbose_name_plural = "Фотограции в мерче"
        ordering = ["id"]

    def __str__(self):
        return f"Фото {self.ambassador.name}"


class Content(models.Model):
    """Модель контента."""

    TYPES = {
        "review": "Отзыв",
        "content": "Контент",
    }
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name="content",
        verbose_name="Амбассадор",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    link = models.URLField(
        verbose_name="Ссылка",
        max_length=5000,
    )
    is_guide_content = models.BooleanField(
        default=False,
        verbose_name="Контент в рамках гайда",
    )
    platform = models.CharField(
        max_length=200,
        verbose_name="Платформа",
        null=True,
    )
    type = models.CharField(
        max_length=200,
        choices=TYPES,
        null=True,
        verbose_name="Тип (отзыв/контент)",
    )
    image = models.ImageField(
        upload_to="content/",
        default="None",
        null=True,
        blank=True,
        verbose_name="Изображение",
    )

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.ambassador.name} на {self.platform}"
