from django.db import models
from settings import settings
from django.utils.timezone import now


class Date_reception(models.Model):

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Doctor',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    time = models.TimeField()


