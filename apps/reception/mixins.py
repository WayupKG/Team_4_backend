from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ReceptionModelMixin(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    pass
