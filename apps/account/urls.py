from rest_framework.routers import SimpleRouter

from .views import UserViewSet, DoctorViewSet, SpecialtyViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register('doctors', DoctorViewSet, 'doctors')
router.register('specialties', SpecialtyViewSet, 'specialty')

urlpatterns = router.urls



