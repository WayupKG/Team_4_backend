from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecialtyViewSet, FeedbackCreateDeleteView


router = DefaultRouter()
router.register('doctors', DoctorViewSet, 'doctors')
router.register('feedback', FeedbackCreateDeleteView, 'feedback')
router.register('specialty', SpecialtyViewSet, 'specialty')


urlpatterns = []

urlpatterns += router.urls