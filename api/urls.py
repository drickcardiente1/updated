from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)
from rest_framework_simplejwt import views as jwt_views

app_name = "api"

urlpatterns = [
    # ex: api/user/login/
    path("otp/", views.OTPView.as_view(), name="OTP"),
    path("login/", views.LoginView.as_view(), name="Login"),
    path('Profile/', views.Profile.as_view(), name="Profile"),
    path("register/", views.RegisterView.as_view(), name="Register"),
    path("reset/sendotp/", views.OTPViewForgotPassword.as_view(), name="reset_user_password"),
    path("reset/password/", views.PasswordResetView.as_view(), name="reset_user_password"),
    # social
]
