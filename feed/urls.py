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

    # Auth URLs
    path('profile/', login_required(RedirectView.as_view(url='/profile/edit/')),
         name='profile'),
    path('profile/edit/', login_required(feed.views.profile.edit.ProfileEditView.as_view()),
         name='profile_edit'),
    path('profile/login/', anonym_required(LoginView.as_view()), name='login'),
    path('profile/logout/', login_required(LogoutView.as_view()), name='logout'),
    path('profile/password_change/', login_required(PasswordChangeView.as_view()), name='password_change'),
    path('profile/password_change/done/', login_required(PasswordChangeDoneView.as_view()), name='password_change_done'),
    path("profile/password_reset/",
         anonym_required(PasswordResetView.as_view(html_email_template_name="emails/registration/password_reset_email.html")),
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

    # Waitlist URLs
    path('waitlist/', feed.views.waitlist.WaitlistView.as_view(), name='waitlist'),
    path('waitlist/success/', feed.views.waitlist.WaitlistSuccessView.as_view(), name='waitlist_success'),

    # API URLs
    path('api/v1/feed/', feed.views.api.FeedItemListView.as_view(), name='api_feed_list'),
    path('api/v1/feed/<int:id>/<str:action>', views.api.FeedItemActions.as_view(),
         name='api_feed_item_toggle_interesting'),

]
