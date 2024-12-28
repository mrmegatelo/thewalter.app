from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

import feed.views.feed.feed_success
from . import views
from .views.decorators import anonym_required

urlpatterns = [
    path("", views.index.Index.as_view(), name="index"),
    # Feed  URLs
    # path(
    #     "feed/", login_required(feed.views.feed.FeedView.as_view()), name="feed_index"
    # ),
    # path(
    #     "feed/items/<int:item_pk>",
    #     login_required(feed.views.feed.FeedView.as_view()),
    #     name="feed_detail",
    # ),
    # path(
    #     "feed/podcasts",
    #     login_required(feed.views.feed.FeedView.as_view(feed_type="podcasts")),
    #     name="feed_podcasts",
    # ),
    # path(
    #     "feed/podcasts/<int:item_pk>",
    #     login_required(feed.views.feed.FeedView.as_view(feed_type="podcasts")),
    #     name="feed_podcast_detail",
    # ),
    # path(
    #     "feed/articles",
    #     login_required(feed.views.feed.FeedView.as_view(feed_type="articles")),
    #     name="feed_articles",
    # ),
    # path(
    #     "feed/articles/<int:item_pk>",
    #     login_required(feed.views.feed.FeedView.as_view(feed_type="articles")),
    #     name="feed_article_detail",
    # ),
    # path(
    #     "feed/videos",
    #     login_required(feed.views.feed.FeedView.as_view(feed_type="videos")),
    #     name="feed_videos",
    # ),
    # path(
    #     "feed/videos/<int:item_pk>",
    #     login_required(feed.views.feed.FeedView.as_view(feed_type="videos")),
    #     name="feed_video_detail",
    # ),
    # path(
    #     "feed/<slug:slug>",
    #     login_required(feed.views.feed.Subscription.as_view()),
    #     name="feed_subscription",
    # ),
    # path(
    #     "feed/<slug:slug>/<int:item_pk>",
    #     login_required(feed.views.feed.Subscription.as_view()),
    #     name="subscription_detail",
    # ),
    # path(
    #     "favorites/",
    #     login_required(feed.views.feed.Favorites.as_view()),
    #     name="favorites",
    # ),
    # path(
    #     "favorites/<int:item_pk>",
    #     login_required(feed.views.feed.Favorites.as_view()),
    #     name="favorites_detail",
    # ),
    # # Feed creation
    # path(
    #     "feed/new/",
    #     login_required(feed.views.feed.FeedCreate.as_view()),
    #     name="new_feed",
    # ),
    # path(
    #     "feed/new/success/",
    #     login_required(feed.views.feed.feed_success.Created.as_view()),
    #     name="feed_success",
    # ),
    # # Collection URLs
    # path(
    #     "collection/<slug:slug>",
    #     login_required(feed.views.collection.CollectionFeedItemsListView.as_view()),
    #     name="collection_feed",
    # ),
    # path(
    #     "collection/new/",
    #     login_required(feed.views.collection.CollectionCreate.as_view()),
    #     name="new_collection",
    # ),
    # path(
    #     "collection/<slug:slug>/update",
    #     login_required(feed.views.collection.CollectionUpdateView.as_view()),
    #     name="collection_update",
    # ),
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
        anonym_required(views.profile.RegistrationView.as_view()),
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
        "api/v1/subscriptions",
        feed.views.api.SubscriptionsView.as_view(),
        name="api_subscriptions",
    ),
    path("api/v1/feed/", feed.views.api.FeedListView.as_view(), name="api_feed_list"),
    path(
        "api/v1/feed/articles",
        feed.views.api.UserFeedList.as_view(feed_type="articles"),
        name="api_feed_articles",
    ),
    path(
        "api/v1/feed/podcasts",
        feed.views.api.UserFeedList.as_view(feed_type="podcasts"),
        name="api_feed_podcasts",
    ),
    path(
        "api/v1/feed/videos",
        feed.views.api.UserFeedList.as_view(feed_type="videos"),
        name="api_feed_videos",
    ),
    path(
        "api/v1/feed/<int:feed_id>/",
        feed.views.api.FeedItemListView.as_view(),
        name="api_feed_feed_list",
    ),
    path(
        "api/v1/feeds/detail/<int:pk>",
        views.api.feed_detail.FeedItemDetailView.as_view(),
        name="api_feed_detail",
    ),
    path(
        "api/v1/feed/favorites",
        feed.views.api.Favorites.as_view(),
        name="api_feed_favorites",
    ),
    path(
        "api/v1/feed/filters/",
        feed.views.api.FeedFilters.as_view(),
        name="api_feed_filters",
    ),
    path(
        "api/v1/feed/types/", feed.views.api.FeedTypes.as_view(), name="api_feed_types"
    ),
    path(
        "api/v1/feed/<int:feed_id>/<str:action>",
        feed.views.api.FeedUnsubscribe.as_view(),
        name="api_feed_action",
    ),
    path(
        "api/v1/feed/actions/<int:pk>/<str:action>",
        views.api.FeedItemActionsView.as_view(),
        name="api_feed_item_toggle_interesting",
    ),
    path(
        "api/v1/feed/parsing_status",
        feed.views.api.ParsingStatus.as_view(),
        name="api_feed_parsing_status",
    ),
    path(
        "api/v1/collection/<int:collection_id>/feed/",
        feed.views.api.CollectionFeed.as_view(),
        name="api_collection_feed",
    ),
    path(
        "api/v1/dialog/hide",
        views.api.dialogs.DialogHide.as_view(),
        name="api_dialog_hide",
    ),
    path(
        "api/v1/dialog/feed/new",
        views.api.dialogs.NewFeed.as_view(),
        name="api_dialog_feed_new",
    ),
    path(
        "api/v1/dialog/collection/new",
        views.api.dialogs.NewCollectionView.as_view(),
        name="api_dialog_collection_new",
    ),
    path(
        "api/v1/dialog/collection/<int:collection_id>/update",
        views.api.dialogs.CollectionUpdateView.as_view(),
        name="api_dialog_collection_edit",
    ),
]
