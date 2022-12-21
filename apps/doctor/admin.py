from django.contrib import admin
from .models import Specialty, Doctor, DoctorAvatar


class TabularInlineImage(admin.TabularInline):
    model = DoctorAvatar
    extra = 1
    fields = ['image']


class DoctorAdmin(admin.ModelAdmin):
    model = Doctor
    inlines = [TabularInlineImage]


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Specialty)
