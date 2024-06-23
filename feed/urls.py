from django.contrib.auth.views import LoginView
from django.urls import path

import feed.views.feed.feed_create
import feed.views.feed.feed_items_list
import feed.views.feed.feed_success
from . import views

urlpatterns = [
    path('', views.index.Index.as_view(), name='index'),

    # Feed  URLs
    path('feed/', feed.views.feed.feed_items_list.FeedItemsListView.as_view(), name='feed_index'),
    path('feed/new/', feed.views.feed.feed_create.Create.as_view(), name='new_feed'),
    path('feed/new/success/', feed.views.feed.feed_success.Created.as_view(), name='feed_success'),

    # Auth URLs
    path('login/', LoginView.as_view(next_page='feed_index'), name='login'),

    # API URLs
    path('api/v1/feed/', feed.views.api.FeedItemListView.as_view(), name='api_feed_list'),
    path('api/v1/feed/<int:id>/<str:action>', views.api.FeedItemActions.as_view(),
         name='api_feed_item_toggle_interesting'),

]
