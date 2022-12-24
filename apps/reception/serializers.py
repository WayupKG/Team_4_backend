from rest_framework import serializers

from .models import Reception


class ReceptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    doctor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reception
        fields = ('id', 'user', 'doctor', 'description', 'date', 'time', 'created_at')


class ReceptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reception
        fields = ('id', 'user', 'doctor', 'description', 'date', 'time')
