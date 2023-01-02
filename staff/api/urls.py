from rest_framework.routers import DefaultRouter
from . import views as staff_views

router = DefaultRouter(trailing_slash=False)

router.register('products', staff_views.ProductViewSet, basename='products')

urlpatterns = router.urls
