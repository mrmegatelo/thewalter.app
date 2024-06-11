from django.views.generic import TemplateView, CreateView, ListView

from feed.forms import FeedForm
from feed.models import Feed


# Create your views here.
class IndexView(ListView):
    model = Feed
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        return context


class FeedSuccess(TemplateView):
    template_name = 'feed/success.html'


class NewFeed(CreateView):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed_success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Feed'
        return context
