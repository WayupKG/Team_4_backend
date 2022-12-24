from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reception(models.Model):
    TIME_CHOICES = (
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
    )
    user = models.ForeignKey(to=User, verbose_name='Patient',
                             related_name='my_receptions', on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=User, verbose_name='Doctor', related_name='receptions',
                               on_delete=models.CASCADE)
    description = models.TextField('Description')
    date = models.DateField(verbose_name='date reception')
    time = models.TimeField('', max_length=28, choices=TIME_CHOICES)
    created_at = models.DateTimeField('Created time', auto_now_add=True)
    updated_at = models.DateTimeField('Updated time', auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Reception'
        verbose_name_plural = 'Receptions'

    def __str__(self):
        return f"{self.date} - {self.time}: {self.user} -> {self.doctor}"
