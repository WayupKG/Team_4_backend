from dataclasses import fields
from email.policy import default
from rest_framework import serializers
from .models import Doctor, DoctorAvatar, Specialty, Rating, Feedback
from django.db.models import Avg


class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Doctor
        exclude = ('email', 'password')
    
    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user 
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['feedbacks'] = FeedbackSerializer(
            instance.feedbacks.all(), many=True
        ).data
        rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        if rating:
            rep['rating'] = round(rating, 1)
        else:
            rep['rating'] = 0.0
        return rep



class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('avatar', 'first_name', 'last_name', 'sur_name', 'specialty')


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = 'all'


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source = 'user.id'
    )
    
    class Meta:
        model = Feedback
        exclude = ['doctor']


class DoctorAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvatar
        fields = 'avatar',


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.id'
    )

    class Meta:
        model = Rating
        fields = ('rating', 'user', 'doctor',)

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError(
                'Wrong value! Rating must be between 1 and 5'
            )
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)
