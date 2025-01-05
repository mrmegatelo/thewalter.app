from django.urls import path

from feed import views

urlpatterns = [
    # API URLs
    path(
        "api/v1/collections/",
        views.api.CollectionListView.as_view(),
        name="api_collection_list",
    ),
    path(
        "api/v1/collections/<int:pk>/",
        views.api.CollectionUpdateView.as_view(),
        name="api_collection_update",
    ),
    path(
        "api/v1/collections/<int:pk>/feed/",
        views.api.CollectionFeedListView.as_view(),
        name="api_collection_feed_list",
    ),
    path(
        "api/v1/subscriptions/",
        views.api.SubscriptionsListView.as_view(),
        name="api_subscriptions_list",
    ),
    path(
        "api/v1/subscriptions/<int:pk>/feed/",
        views.api.SubscriptionsFeedListView.as_view(),
        name="api_subscription_feed_list",
    ),
    path(
        "api/v1/feed/",
        views.api.FeedListView.as_view(),
        name="api_feed_list",
    ),
    path(
        "api/v1/feed/<int:pk>/",
        views.api.FeedItemUpdateView.as_view(),
        name="api_feed_item_update",
    ),
    path(
        "api/v1/feed/<int:feed_item_pk>/actions/<str:action>/",
        views.api.FeedItemActionView.as_view(),
        name="api_feed_item_actions",
    ),
]
