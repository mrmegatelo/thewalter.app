from django.views.generic import TemplateView, CreateView

from feed.forms import FeedForm


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        context['new_feed_form'] = FeedForm()
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
