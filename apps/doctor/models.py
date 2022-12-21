import email
from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Specialty(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Doctor(models.Model):
    TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    email = ...
    password = ...
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    sur_name = models.CharField(max_length=200)
    specialty = models.ForeignKey(
        to=Specialty,
        on_delete=models.CASCADE,
        related_name='doctors')
    experience = models.IntegerField(default=1)
    avatar = models.ImageField(upload_to='doctor_avatar')
    phone = models.IntegerField(max_length=10)
    user_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='doctor')

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.sur_name}"

    
class DoctorAvatar(models.Model):
    avatar = models.ImageField(upload_to='doctor_avatar')
    doctor = models.ForeignKey(
        to=Doctor,
        on_delete=models.CASCADE,
        related_name='avatars'
    )

    def __str__(self) -> str:
        return f"Avatart to {self.last_name} {self.first_name} {self.sur_name}"
    

class Feedback(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    doctor = models.ForeignKey(
        to=Doctor,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.last_name} {self.first_name}"


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, 
        blank=True, 
        null=True)
    doctor = models.ForeignKey(
        to=Doctor,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self):
        return str(self.rating)
