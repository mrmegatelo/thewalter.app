from django.views.generic import CreateView

from feed.forms import FeedForm
from feed.views.mixins import ProtectedViewMixin


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
