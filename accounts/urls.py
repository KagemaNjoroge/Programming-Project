from django.urls import path
from .views import (
    UserManagement,
    login_view,
    profile,
    VerificationCodesView,
    email_verification_page,
    register_user,
    logout_view
)

app_name = "accounts"
urlpatterns = [
    path("user/<str:username>/", UserManagement.as_view(), name="user"),
    path("user/", UserManagement.as_view(), name="user"),
    path("login/", login_view, name="login"),
    path("profile/", profile, name="profile"),
    path(
        "verification-codes/",
        VerificationCodesView.as_view(),
        name="verification-codes",
    ),
    path("verify/", email_verification_page, name="verify"),
    path("register/", register_user, name="register"),
    path("logout/", logout_view, name="logout"),
]
