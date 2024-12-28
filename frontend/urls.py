from django.urls import path

from frontend import views

urlpatterns = [
    path('test<path:subpath>', views.TestView.as_view(), name='test'),
]