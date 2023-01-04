from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views as staff_views

router = DefaultRouter(trailing_slash=False)

router.register('products', staff_views.ProductViewSet, basename='products')
router.register('serial-keys', staff_views.SerialKeyViewSet, basename='serial-keys')
router.register('product/content', staff_views.ProductContentViewSet, basename='product-content')

urlpatterns = [
    path('search-product', staff_views.SearchProductView.as_view(), name='search-product'),
    path('search-videos', staff_views.SearchVideoView.as_view(), name='search-videos'),
]

urlpatterns += router.urls
