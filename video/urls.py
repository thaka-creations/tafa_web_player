from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, ProductViewSet, ListProductVideoApiView

router = DefaultRouter(trailing_slash=False)

router.register(r'videos', VideoViewSet, basename='videos')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
   path('products/list-product-videos', ListProductVideoApiView.as_view(), name='list-product-videos')
]

urlpatterns += router.urls
