from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

import feed.views.feed.feed_create
import feed.views.feed.feed_success
from . import views
from .views.decorators import anonym_required

urlpatterns = [
    path('', views.index.Index.as_view(), name='index'),
    # Feed  URLs
    path('feed/', login_required(feed.views.feed.feed_items_list.FeedItemsListView.as_view()), name='feed_index'),
    path('feed/new/', login_required(feed.views.feed.feed_create.Create.as_view()), name='new_feed'),
    path('feed/new/success/', login_required(feed.views.feed.feed_success.Created.as_view()), name='feed_success'),
    path('feed/<slug:slug>', login_required(feed.views.feed.subscription.Subscription.as_view()),
         name='feed_subscription'),

    # Auth URLs
    path('profile/', login_required(RedirectView.as_view(url='/profile/edit/')),
         name='profile'),
    path('profile/edit/', login_required(feed.views.profile.edit.ProfileEditView.as_view()),
         name='profile_edit'),
    path('profile/login/', anonym_required(LoginView.as_view()), name='login'),
    path('profile/logout/', login_required(LogoutView.as_view()), name='logout'),

    # Password change URLs
    path('profile/password_change/', login_required(PasswordChangeView.as_view()), name='password_change'),
    path('profile/password_change/done/', login_required(PasswordChangeDoneView.as_view()),
         name='password_change_done'),

    # Password reset URLs
    path("profile/password_reset/",
         anonym_required(
             PasswordResetView.as_view(html_email_template_name="emails/registration/password_reset_email.html")),
         name="password_reset"
         ),
    path(
        "profile/password_reset/done/",
        anonym_required(PasswordResetDoneView.as_view()),
        name="password_reset_done",
    ),
    path(
        "profile/reset/<uidb64>/<token>/",
        anonym_required(PasswordResetConfirmView.as_view()),
        name="password_reset_confirm",
    ),
    path(
        "profile/reset/done/",
        anonym_required(PasswordResetCompleteView.as_view()),
        name="password_reset_complete",
    ),

    # Invite accept URLs
    path(
        "profile/invite/<uidb64>/<token>/set_username",
        anonym_required(feed.views.profile.invite_username.InviteUsernameView.as_view()),
        name="invite_accept_username"
    ),
    path(
        "profile/invite/<uidb64>/<token>/set_password",
        anonym_required(PasswordResetConfirmView.as_view(
            template_name='profile/invite_password.html',
            success_url='/profile/invite/done'
        )),
        name="invite_accept_password"
    ),
    path(
        "profile/invite/done",
        anonym_required(PasswordResetCompleteView.as_view(
            title='Welcome🥳',
            template_name='profile/invite_done.html',
        )),
        name="invite_accept_complete"
    ),

    # Waitlist URLs
    path('waitlist/', feed.views.waitlist.WaitlistView.as_view(), name='waitlist'),
    path('waitlist/success/', feed.views.waitlist.WaitlistSuccessView.as_view(), name='waitlist_success'),

    # API URLs
    path('api/v1/feed/', feed.views.api.UserFeedList.as_view(), name='api_feed_list'),
    path('api/v1/feed/filters/', feed.views.api.FeedFilters.as_view(), name='api_feed_filters'),
    path('api/v1/feed/<int:feed_id>/', feed.views.api.FeedItemListView.as_view(), name='api_feed_feed_list'),
    path('api/v1/feed/<int:feed_id>/<str:action>', feed.views.api.FeedUnsubscribe.as_view(), name='api_feed_action'),
    path('api/v1/feed/<int:feed_id>/<int:feed_item_id>/<str:action>', views.api.FeedItemActions.as_view(),
         name='api_feed_item_toggle_interesting'),
]
