from rest_framework.routers import SimpleRouter

from .views import UserViewSet, FeedbackViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register('feedback', FeedbackViewSet)

urlpatterns = router.urls



