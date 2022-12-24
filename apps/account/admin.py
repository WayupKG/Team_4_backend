from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Feedback, Specialty

User = get_user_model()


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'rating', 'created_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'user_type', 'is_active')


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title',)
