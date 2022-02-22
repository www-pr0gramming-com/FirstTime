from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from app.views import SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("app.urls", namespace="app")),
    path("app2/", include("app2.urls", namespace="app2")),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("singup/", SignupView.as_view(), name="singup"),
    # password reset ####################
    path("reset-password/", PasswordResetView.as_view(), name="reset-password"),
    path(
        "password-reset-done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # ####################
    path("", TemplateView.as_view(template_name="landing.html")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
