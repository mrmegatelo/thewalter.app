from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

import feed
from .views.decorators import anonym_required

urlpatterns = [
    path("", feed.views.index.Index.as_view(), name="index"),
    # Auth URLs
    path(
        "profile/",
        login_required(RedirectView.as_view(url="/profile/edit/")),
        name="profile",
    ),
    path(
        "profile/edit/",
        login_required(feed.views.profile.edit.ProfileEditView.as_view()),
        name="profile_edit",
    ),
    path(
        "profile/register/",
        anonym_required(feed.views.profile.RegistrationView.as_view()),
        name="register",
    ),
    path(
        "profile/activate/",
        feed.views.profile.ActivationView.as_view(),
        name="django_registration_activate",
    ),
    path(
        "profile/activate/complete/",
        feed.views.profile.ActivationSuccessView.as_view(),
        name="django_registration_activation_complete",
    ),
    path("profile/", include("django_registration.backends.activation.urls")),
    path("profile/", include("django.contrib.auth.urls")),
    # Invite accept URLs
    path(
        "profile/invite/<uidb64>/<token>/set_username",
        anonym_required(
            feed.views.profile.invite_username.InviteUsernameView.as_view()
        ),
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
    # API URLs
    path(
        "api/v1/collections/",
        feed.views.api.CollectionListView.as_view(),
        name="api_collection_list",
    ),
    path(
        "api/v1/collections/<int:pk>/",
        feed.views.api.CollectionUpdateView.as_view(),
        name="api_collection_update",
    ),
    path(
        "api/v1/collections/<int:pk>/feed/",
        feed.views.api.CollectionFeedListView.as_view(),
        name="api_collection_feed_list",
    ),
    path(
        "api/v1/subscriptions/",
        feed.views.api.SubscriptionsListView.as_view(),
        name="api_subscriptions_list",
    ),
    path(
        "api/v1/subscriptions/<int:pk>/feed/",
        feed.views.api.SubscriptionsFeedListView.as_view(),
        name="api_subscription_feed_list",
    ),
    path(
        "api/v1/feed/",
        feed.views.api.FeedListView.as_view(),
        name="api_feed_list",
    ),
    path(
        "api/v1/feed/<int:pk>/",
        feed.views.api.FeedItemUpdateView.as_view(),
        name="api_feed_item_update",
    ),
    path(
        "api/v1/feed/<int:feed_item_pk>/actions/<str:action>/",
        feed.views.api.FeedItemActionView.as_view(),
        name="api_feed_item_actions",
    ),
]
