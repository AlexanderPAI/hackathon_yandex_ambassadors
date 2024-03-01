from django.db import models
from django.utils.text import slugify

# TODO Поле gender, отдельные таблицы или enums


class GroupPurposeProgramStatusBase(models.Model):
    """Describes models base class Group, Purpose, Program and Status"""

    name = models.CharField(max_length=75)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Group(GroupPurposeProgramStatusBase):
    """Describes Group entity"""

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Purpose(GroupPurposeProgramStatusBase):
    """Describes Purpose entity"""

    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class Program(GroupPurposeProgramStatusBase):
    """Describes Program entity"""

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"


class Status(GroupPurposeProgramStatusBase):
    """Describes Status entity"""

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Address(models.Model):
    """Describes Address entity"""

    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

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

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    clothing_size = models.CharField(max_length=2)
    shoe_size = models.CharField(max_length=4)
    education = models.CharField(max_length=120)
    job = models.CharField(max_length=120)
    email = models.EmailField(max_length=30)
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="ambassadors"
    )
    phone_number = models.CharField(max_length=14)
    telegram_id = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=14, null=True, blank=True)
    activity = models.CharField(max_length=255)
    blog_link = models.URLField(max_length=255, null=True, blank=True)
    # TODO ForeignKey - tutor field
    tutor = models.IntegerField(default=0)
    onbording_status = models.BooleanField(default=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="ambassadors",
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="ambassadors",
    )
    purpose = models.ForeignKey(
        Purpose,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="ambassadors",
    )
    about_me = models.TextField(null=True, blank=True)
    # TODO ForeignKey promocode field
    promocode = models.IntegerField(default=0)
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name="ambassadors",
        verbose_name="Группа",
    )

    class Meta:
        verbose_name = "Амбассадор"
        verbose_name_plural = "Амбассадоры"

    def __str__(self):
        return (
            f"{self.name} ({self.status}) {self.tutor} {self.program} " f"{self.email}"
        )


class AmbassadorMerch(models.Model):
    """Describe Ambassador and Merch relations"""

    # TODO ForeignKey merch field
    merch = models.IntegerField(default=0)
    ambassador = models.ForeignKey(
        Ambassador, on_delete=models.CASCADE, related_name="Merch"
    )
    amount_of_shipments = models.IntegerField()

    def __str__(self):
        return f"{self.ambassador} {self.merch} {self.amount_of_shipments}"
