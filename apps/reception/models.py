from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reception(models.Model):
    patient = models.ForeignKey(to=User, verbose_name='Patient',
                                related_name='my_receptions', on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=User, verbose_name='Doctor', related_name='receptions',
                               on_delete=models.CASCADE)
    description = models.TextField('Description')
    date_reception = models.ForeignKey('DateReception', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created time', auto_now_add=True)
    updated_at = models.DateTimeField('Updated time', auto_now=True)

    class Meta:
        verbose_name = 'Reception'
        verbose_name_plural = 'Receptions'

    def __str__(self):
        return f"{self.date_reception} -> {self.patient}"


class DateReception(models.Model):
    doctor = models.ForeignKey(to=User, verbose_name='Doctor', on_delete=models.CASCADE,
                               related_name='date_receptions')
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        verbose_name = 'Date reception'
        verbose_name_plural = 'Date receptions'

    def __str__(self):
        return f"{self.doctor}: {self.date} -> {self.time}"



