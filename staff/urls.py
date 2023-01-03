from django.urls import path
from staff import views as staff_views

urlpatterns = [
    path('dashboard', staff_views.DashboardView.as_view(), name='dashboard'),
    path('products', staff_views.ListProductView.as_view(), name='products'),
    path('serial-keys', staff_views.ListSerialKeyView.as_view(), name='serial-keys'),
    path('serial-keys/generate', staff_views.GenerateSerialKeyView.as_view(), name='generate-serial-key'),
    path('retrieve-product/<pk>', staff_views.RetrieveProductView.as_view(), name='retrieve-product'),
]
