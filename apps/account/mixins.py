from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class UserMixinSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """Для создание CRUD user"""
    pass
