from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_1 = "ROLE 1"
ROLE_2 = "ROLE 2"
ROLE_CHOICES = (
    (ROLE_1, "Менеджер"),
    (ROLE_2, "Амбассадор"),
)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=150,
        choices=ROLE_CHOICES,
        default=ROLE_1,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.get_full_name()
