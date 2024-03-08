import random

from django.utils import timezone

from promo.models import MerchApplication

LENGTH = 6


def generate_application_number():
    """Generates random ID for a merch application."""
    time = timezone.localdate()
    random_int = random.randrange(100000, 1000000)
    number = str(time) + "-" + str(random_int)
    if MerchApplication.objects.filter(application_number=number):
        number += str(random.randrange(100000, 1000000))
    return number
