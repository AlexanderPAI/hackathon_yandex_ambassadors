from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_1 = "ROLE 1"
ROLE_CHOICES = (
    (ROLE_1, "Роль 1"),
)


class User(AbstractUser):
    role = models.CharField(
        max_length=150, choices=ROLE_CHOICES, default=ROLE_1, verbose_name="Роль"
    )

    def __str__(self):
        return self.get_full_name()
