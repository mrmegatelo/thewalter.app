from django.views.generic import TemplateView, CreateView, ListView

from feed.forms import FeedForm
from feed.models import Feed
from feed.views.mixins import ProtectedViewMixin


# Create your views here.
class Index(ProtectedViewMixin, ListView):
    model = Feed
    template_name = 'feed/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        return context


class Created(ProtectedViewMixin, TemplateView):
    template_name = 'feed/success.html'


class Create(ProtectedViewMixin, CreateView):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed/new/success/'

    def get_initial(self):
        return {'created_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Feed'
        return context
