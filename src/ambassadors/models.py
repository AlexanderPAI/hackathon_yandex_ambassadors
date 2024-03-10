from django.db import models
from django.utils.text import slugify

from users.models import User


class CommonAbstractModel(models.Model):
    """Describes common abstract models for Purpose, Program, Status, Activity"""

    class Meta:
        abstract = True

    slug = models.SlugField(max_length=75, unique=True, verbose_name="Slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Purpose(CommonAbstractModel):
    """Describes Purpose entity"""

    name = models.CharField(max_length=75, verbose_name="Цель в Практикуме")
    personal_purpose = models.TextField(
        null=True, blank=True, verbose_name="Moя цель в Практикуме"
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.name


class Program(CommonAbstractModel):
    """Describes Program entity"""

    name = models.CharField(max_length=75, verbose_name="Программа в Практикуме")

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return self.name


class Status(CommonAbstractModel):
    """Describes Status entity"""

    name = models.CharField(max_length=75, verbose_name="Статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Activity(CommonAbstractModel):
    """Describes Activity entity"""

    name = models.CharField(max_length=75, verbose_name="Цель Амбассадорства")

    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Активности"

    def __str__(self):
        return self.name


class Address(models.Model):
    """Describes Address entity"""

    postal_code = models.CharField(max_length=6, verbose_name="Индекс")
    country = models.CharField(max_length=50, verbose_name="Страна")
    city = models.CharField(max_length=50, verbose_name="Город")
    street = models.CharField(max_length=50, verbose_name="Улица")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return f"{self.postal_code} {self.country} {self.city} {self.street}"


class Ambassador(models.Model):
    """Describes Ambassador entity"""

    GENDER_CHOICES = (
        ("М", "Мужской"),
        ("Ж", "Женский"),
    )

    CLOTHES_SIZE_CHOICES = (
        ("XS", "Extra Small"),
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    name = models.CharField(max_length=50, verbose_name="ФИО")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    clothing_size = models.CharField(
        max_length=2, choices=CLOTHES_SIZE_CHOICES, verbose_name="Размер одежды"
    )
    shoe_size = models.CharField(max_length=4, verbose_name="Размер обуви")
    education = models.CharField(max_length=120, verbose_name="Образование")
    job = models.CharField(max_length=120, verbose_name="Место работы")
    email = models.EmailField(max_length=30, verbose_name="Email")
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="ambassadors",
        verbose_name="Адрес",
    )
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    telegram_id = models.CharField(max_length=30, verbose_name="Telegram")
    whatsapp = models.CharField(
        max_length=14, null=True, blank=True, verbose_name="Whatsapp"
    )
    activity = models.ManyToManyField(
        Activity,
        through="AmbassadorActivity",
        related_name="ambassadors",
        verbose_name="Цель Амбассадорства",
    )
    blog_link = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="Ссылка на блог"
    )
    tutor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ambassadors",
        verbose_name="Наставник",
    )
    onboarding_status = models.BooleanField(
        default=False, verbose_name="Onboarding статус"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="ambassadors",
        verbose_name="Статус",
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="ambassadors",
        verbose_name="Программа в Практикуме",
    )
    purpose = models.ManyToManyField(
        Purpose,
        through="AmbassadorPurpose",
        related_name="ambassadors",
        verbose_name="Цель в Практикуме",
    )

    about_me = models.TextField(null=True, blank=True, verbose_name="О себе")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Амбассадор"
        verbose_name_plural = "Амбассадоры"

    def __str__(self):
        return f"{self.name} ({self.status}) {self.tutor} {self.program} {self.email}"


class AmbassadorActivity(models.Model):
    """Describe Ambassador and Activity relations"""

    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
    )


class AmbassadorPurpose(models.Model):
    """Describe Ambassador and Purpose relations"""

    ambassador = models.ForeignKey(Ambassador, on_delete=models.CASCADE)

    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
