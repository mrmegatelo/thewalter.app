from django.contrib.auth.decorators import login_required
from django.urls import path

from frontend import views

urlpatterns = [
    path('feed<path:subpath>', login_required(views.TestView.as_view()), name='feed_index'),
]