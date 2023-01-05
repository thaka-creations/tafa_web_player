from django.urls import path
from . import views as user_views

urlpatterns = [
    path('register', user_views.RegisterUserView.as_view(), name='register'),
    path('verify-otp', user_views.VerifyOtpCodeView.as_view(), name='verify-otp'),
    path('login', user_views.LoginView.as_view(), name='login'),
]
