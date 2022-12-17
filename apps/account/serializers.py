from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from .tasks import send_activation_code
from .services.validations import email_validator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=128, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password', 'password_confirm')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Email already in use'
            )
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code.delay(user.email, user.activation_code)
        validated_data.get('first_name').capitalize()
        validated_data.get('last_name').capitalize()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_pass_confirm = serializers.CharField(max_length=128, required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Wrong password'
            )
        return old_password 

    def validate(self, attrs: dict):
        new_password = attrs.get('new_password')
        new_pass_confirm = attrs.get('new_pass_confirm')
        if new_password != new_pass_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255,
                                   validators=[email_validator])

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Password restore',
            message=f'Your code for password restore {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )


class SetRestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=255,
        validators=[email_validator]
    )
    code = serializers.CharField(min_length=1, max_length=8, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_pass_confirm = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        if not User.objects.filter(email=attrs.get('email'),
                                   activation_code=attrs.get('code')).exists():
            raise serializers.ValidationError('Wrong code')
        new_password = attrs.get('new_password')
        new_pass_confirm = attrs.get('new_pass_confirm')
        if new_password != new_pass_confirm:
            raise serializers.ValidationError(
                'Password do not match'
            )
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.activation_code = ''
        user.save()
