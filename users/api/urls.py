from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views as user_views

router = DefaultRouter(trailing_slash=False)
router.register(r'auth', user_views.AuthenticationViewSet, basename='auth')
router.register(r'account', user_views.UserViewSet, basename='account')

urlpatterns = [
    path('register', user_views.RegisterUserView.as_view(), name='register'),
    path('verify-otp', user_views.VerifyOtpCodeView.as_view(), name='verify-otp'),
    path('resend-otp', user_views.ResendOtpCodeView.as_view(), name='resend-otp'),
]

urlpatterns += router.urls
