from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def email_validator(email):
    if not User.objects.filter(email=email).exists():
        raise serializers.ValidationError('User with this email does not exist')
    return email
