from django.urls import path
from staff import views as staff_views

urlpatterns = [
    path('dashboard', staff_views.DashboardView.as_view(), name='dashboard'),
]
