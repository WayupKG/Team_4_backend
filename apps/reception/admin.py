from django.contrib import admin

from .models import Reception


@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date', 'time', 'created_at')
