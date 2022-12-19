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


class Reception(models.Model):

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Patient',
        related_name='patients',
        on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Doctor',
        related_name='doctors',
        on_delete=models.CASCADE
    )
    description = models.CharField(
        'Text',
        max_length=300,
        null=True
    )
    date_reception = models.ForeignKey(
        'Date_reception',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField('Created_time', default=now)
    updated_at = models.DateTimeField('Update_time', blank=True, null=True)
