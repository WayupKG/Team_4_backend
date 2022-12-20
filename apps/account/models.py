from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string

from .managers import UserManager


class User(AbstractBaseUser):
    TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    email = models.EmailField('Email', max_length=255, unique=True)
    first_name = models.CharField('First_name', max_length=50)
    last_name = models.CharField('Last_name', max_length=50)
    phone = models.CharField('Phone', max_length=50)
    user_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='user')
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    activation_code = models.CharField(max_length=8, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def get_user_type_value(self):
        return dict(self.TYPE_CHOICES).get(self.user_type)

    def has_module_perms(self, app_label) -> models.BooleanField:
        return self.is_staff

    def has_perm(self, obj=None) -> models.BooleanField:
        return self.is_staff

    def create_activation_code(self) -> None:
        code = get_random_string(length=8)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code 
        self.save()


class Feedback(models.Model):
    content = models.TextField()
    patient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='patient_feedback',
        null=True
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='feedback',
        null=True
    )
    replies = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient}'


