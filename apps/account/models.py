from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from .managers import UserManager
from .services import constants as cns
from .services.upload_to_file import avatar_img


class Specialty(models.Model):
    title = models.CharField(max_length=255, unique=True)

    objects = models.Manager()

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'


class User(AbstractBaseUser):
    TYPE_CHOICES = (
        (cns.DOCTOR, 'Doctor'),
        (cns.USER, 'User'),
        (cns.ADMIN, 'Admin'),
    )
    email = models.EmailField('Email', max_length=255, unique=True)
    first_name = models.CharField('First_name', max_length=50)
    last_name = models.CharField('Last_name', max_length=50)
    phone = models.CharField('Phone', max_length=50)
    specialty = models.ForeignKey(to=Specialty, on_delete=models.CASCADE,
                                  related_name='doctors', null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    avatar = ProcessedImageField(verbose_name='avatar', upload_to=avatar_img,
                                 format='webp', options={'quality': 90})
    user_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=cns.USER)
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
    RATING_CHOICES = (
        (cns.ONE, '1'),
        (cns.TWO, '2'),
        (cns.THREE, '3'),
        (cns.FOUR, '4'),
        (cns.FIVE, '5')
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='feedbacks_user')
    doctor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'doctor',)
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f"Feedback from {self.user.last_name} {self.user.first_name}"