from django.urls import path
from .views import LoginView, LogoutView, RegisterView, ChangePasswordView, PasswordResetView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("auth/password-reset/", PasswordResetView.as_view(), name="password_reset"),
]