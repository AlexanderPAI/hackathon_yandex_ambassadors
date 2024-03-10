from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from ambassadors.models import Ambassador
from users.models import User


class MerchCategory(models.Model):
    """Describes merch categories."""

    name = models.CharField("Name", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Категория мерча"
        verbose_name_plural = "Категории мерча"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        """Makes slug from a name (cyrillic letters are acceptable too)."""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Merch(models.Model):
    """
    Describes merch species.
    If a parent merch category has been deleted, the associated merch species
    will be deleted as well.
    """

    name = models.CharField("Name", max_length=100)
    category = models.ForeignKey(
        MerchCategory,
        on_delete=models.CASCADE,
        related_name="merch",
        verbose_name="Category",
    )
    slug = models.SlugField("Slug", max_length=100, unique=True, blank=True)
    size = models.CharField("Size", max_length=20, blank=True)
    cost = models.FloatField("Cost", validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Мерч"
        verbose_name_plural = "Мерч"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "size"], name="name_size_unique_merch"
            )
        ]
        ordering = ["id"]

    def save(self, *args, **kwargs):
        """Makes slug from a name and size (cyrillic letters are acceptable too)."""
        if not self.slug:
            self.slug = f"{slugify(self.name, allow_unicode=True)}{self.size}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.size:
            return f"{self.name} {self.size}"
        return self.name


class Promocode(models.Model):
    """Describes ambassadors' promocodes."""

    code = models.CharField("Code", max_length=20, unique=True)
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name="promocodes",
        verbose_name="Ambassador",
    )
    created = models.DateTimeField("Creation time", default=timezone.now)
    is_active = models.BooleanField("Is active", default=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ["id"]

    def __str__(self):
        return self.code


class MerchApplication(models.Model):
    """Describes applications for sending merch to ambassadors."""

    application_number = models.CharField("Number", max_length=50, unique=True)
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name="merch_applications",
        verbose_name="Ambassador",
    )
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="merch_applications",
        verbose_name="User",
    )
    created = models.DateTimeField("Creation time", default=timezone.now)
    merch = models.ManyToManyField(
        Merch,
        through="MerchInApplication",
        related_name="applications",
        verbose_name="Merch",
    )

    class Meta:
        verbose_name = "Заявка на мерч"
        verbose_name_plural = "Заявки на мерч"

    def __str__(self):
        return self.application_number


class MerchInApplication(models.Model):
    """Describes m2m connections between the MerchApplication and Merch models."""

    application = models.ForeignKey(
        MerchApplication,
        on_delete=models.CASCADE,
        related_name="merch_in_applications",
        verbose_name="Application",
    )
    merch = models.ForeignKey(
        Merch,
        on_delete=models.CASCADE,
        related_name="merch_in_applications",
        verbose_name="Merch",
    )
    quantity = models.PositiveIntegerField(
        "Quantity",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = "Мерч в заявках"
        verbose_name_plural = "Мерч в заявках"

    def __str__(self):
        return f"{self.application}-{self.merch}-{self.quantity}"
