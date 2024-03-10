import random

from django.utils import timezone

from promo.models import MerchApplication

YEAR_MONTHS = [
    ("january", 1, "январь"),
    ("february", 2, "февраль"),
    ("march", 3, "март"),
    ("april", 4, "апрель"),
    ("may", 5, "май"),
    ("june", 6, "июнь"),
    ("july", 7, "июль"),
    ("august", 8, "август"),
    ("september", 9, "сентябрь"),
    ("october", 10, "октябрь"),
    ("november", 11, "ноябрь"),
    ("december", 12, "декабрь"),
]

LENGTH = 6


def generate_application_number():
    """Generates random ID for a merch application."""
    time = timezone.localdate()
    random_int = random.randrange(100000, 1000000)
    number = str(time) + "-" + str(random_int)
    if MerchApplication.objects.filter(application_number=number):
        number += str(random.randrange(100000, 1000000))
    return number
