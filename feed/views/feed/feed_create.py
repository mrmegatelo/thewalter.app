from django.views.generic import CreateView
from django.utils.translation import gettext_noop as _

from feed.forms import FeedForm
from feed.views.mixins import ProtectedViewMixin, PageMetaMixin


class Create(ProtectedViewMixin, CreateView, PageMetaMixin):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed/new/success/'
    title = _('New Feed')

    def get_initial(self):
        return {'created_by': self.request.user}
