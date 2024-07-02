from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from django.contrib.auth.decorators import login_required

import feed.views.feed.feed_create
import feed.views.feed.feed_success
from . import views


urlpatterns = [
    path('', views.index.Index.as_view(), name='index'),
    # Feed  URLs
    path('feed/', feed.views.feed.feed_items_list.FeedItemsListView.as_view(), name='feed_index'),
    path('feed/new/', feed.views.feed.feed_create.Create.as_view(), name='new_feed'),
    path('feed/new/success/', feed.views.feed.feed_success.Created.as_view(), name='feed_success'),

    # Auth URLs
    path('profile/', login_required(feed.views.profile.index.ProfileIndexView.as_view()),
         name='profile'),
    path('profile/edit/', login_required(feed.views.profile.edit.ProfileEditView.as_view()),
         name='profile_edit'),
    path('profile/login/', LoginView.as_view(), name='login'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('profile/password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("profile/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "profile/password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "profile/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "profile/reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    # Waitlist URLs
    path('waitlist/', feed.views.waitlist.WaitlistView.as_view(), name='waitlist'),
    path('waitlist/success/', feed.views.waitlist.WaitlistSuccessView.as_view(), name='waitlist_success'),

    # API URLs
    path('api/v1/feed/', feed.views.api.FeedItemListView.as_view(), name='api_feed_list'),
    path('api/v1/feed/<int:id>/<str:action>', views.api.FeedItemActions.as_view(),
         name='api_feed_item_toggle_interesting'),

]
