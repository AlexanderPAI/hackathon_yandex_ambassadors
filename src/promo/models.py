from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


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

    # the name field is non-unique so that we can store merch items with the same names,
    # but different sizes, but the name and size combination must be unique
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
        return self.name


class Promocode(models.Model):
    """Describes ambassadors' promocodes."""

    code = models.CharField("Code", max_length=20, unique=True)
    # TODO: make it ForeignKey referencing Ambassador model, on_delete=models.CASCADE,
    # related_name="promocodes"
    ambassador = models.IntegerField(verbose_name="Ambassador")
    created = models.DateTimeField("Creation time", default=timezone.now)
    is_active = models.BooleanField("Is active", default=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ["id"]

    def __str__(self):
        return self.code
