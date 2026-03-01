"""URLs for account-related views (login, signup, logout, password reset)."""
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("login/", views.EmailLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("django.contrib.auth.urls")),
]
