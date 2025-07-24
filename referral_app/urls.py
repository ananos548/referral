from rest_framework.routers import SimpleRouter

from referral_app.views import UserProfileViewSet


router = SimpleRouter()
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = router.urls
