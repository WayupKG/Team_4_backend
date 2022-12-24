from rest_framework.generics import get_object_or_404

from django.contrib.auth import get_user_model

from apps.account.services import constants as cns
from apps.reception.models import Reception

User = get_user_model()


def get_receptions(user_type, pk):
    if user_type == cns.USER:
        user = get_object_or_404(User, user_type=user_type, pk=pk)
        return Reception.objects.filter(user=user)
    elif user_type == cns.DOCTOR:
        doctor = get_object_or_404(User, user_type=user_type, pk=pk)
        return Reception.objects.filter(doctor=doctor)
    return None
