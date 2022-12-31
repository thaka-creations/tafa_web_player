from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, ProductViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'videos', VideoViewSet, basename='videos')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = router.urls
