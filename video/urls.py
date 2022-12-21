from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'videos', VideoViewSet, basename='videos')

urlpatterns = router.urls
