from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.urls import path, include
from django.views.generic import RedirectView

from frontend import views
from frontend.views.decorators import anonym_required

urlpatterns = [
    path("", views.index.Index.as_view(), name="index"),
    # Main SPA view
    path(
        "feed<path:subpath>",
        login_required(views.spa.SpaView.as_view()),
        name="feed_index",
    ),
    # Auth URLs
    path(
        "profile/",
        login_required(RedirectView.as_view(url="/profile/edit/")),
        name="profile",
    ),
    path(
        "profile/edit/",
        login_required(views.profile.edit.ProfileEditView.as_view()),
        name="profile_edit",
    ),
    path(
        "profile/register/",
        anonym_required(views.profile.RegistrationView.as_view()),
        name="register",
    ),
    path(
        "profile/activate/",
        views.profile.ActivationView.as_view(),
        name="django_registration_activate",
    ),
    path(
        "profile/activate/complete/",
        views.profile.ActivationSuccessView.as_view(),
        name="django_registration_activation_complete",
    ),
    path("profile/", include("django_registration.backends.activation.urls")),
    path("profile/", include("django.contrib.auth.urls")),
    # Invite accept URLs
    path(
        "profile/invite/<uidb64>/<token>/set_username",
        anonym_required(views.profile.invite_username.InviteUsernameView.as_view()),
        name="invite_accept_username",
    ),
    path(
        "profile/invite/<uidb64>/<token>/set_password",
        anonym_required(
            PasswordResetConfirmView.as_view(
                template_name="profile/invite_password.html",
                success_url="/profile/invite/done",
            )
        ),
        name="invite_accept_password",
    ),
    path(
        "profile/invite/done",
        anonym_required(
            PasswordResetCompleteView.as_view(
                title="Welcome🥳",
                template_name="profile/invite_done.html",
            )
        ),
        name="invite_accept_complete",
    ),
]