from django.urls import path
from users import views as user_views

urlpatterns = [
    path('login', user_views.LoginView.as_view()),
]
