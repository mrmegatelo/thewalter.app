from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from feed.forms import FeedForm
from feed.models import Feed


class ProtectedViewMixin(LoginRequiredMixin):
    login_url = '/login/'


# Create your views here.
class IndexView(ProtectedViewMixin, ListView):
    model = Feed
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        return context


class FeedSuccess(ProtectedViewMixin, TemplateView):
    template_name = 'feed/success.html'


class NewFeed(ProtectedViewMixin, CreateView):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed_success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Feed'
        return context
