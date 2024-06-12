from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_feed/', views.NewFeed.as_view(), name='new_feed'),
    path('feed_success/', views.FeedSuccess.as_view(), name='feed_success'),

    path('login/', LoginView.as_view(next_page='index'), name='login'),
]
