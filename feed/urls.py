from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_feed/', views.NewFeed.as_view(), name='new_feed'),
]
