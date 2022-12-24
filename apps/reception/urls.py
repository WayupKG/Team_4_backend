from rest_framework.routers import SimpleRouter

from .views import ReceptionViewSet

router = SimpleRouter()

router.register('receptions', ReceptionViewSet)

urlpatterns = router.urls



