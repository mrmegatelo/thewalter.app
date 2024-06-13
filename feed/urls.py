from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.Index.as_view(), name='index'),

    path('feed/', views.feed.Index.as_view(), name='feed_index'),
    path('feed/new/', views.feed.Create.as_view(), name='new_feed'),
    path('feed/new/success/', views.feed.Created.as_view(), name='feed_success'),

    path('login/', LoginView.as_view(next_page='feed_index'), name='login'),
]
