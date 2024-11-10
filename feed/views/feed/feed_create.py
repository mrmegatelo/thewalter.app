from django.views.generic import FormView
from django.utils.translation import gettext_noop as _

from feed.forms import FeedForm
from feed.utils.helpers import normalize_url
from feed.views.mixins import PageMetaMixin, FeedContextMixin, FeedFiltersMixin


class FeedCreate(FormView, PageMetaMixin, FeedContextMixin, FeedFiltersMixin):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed/new/success/?url={url}'
    title = _('My feed')

    def get_success_url(self):
        return self.success_url.format(url=self.get_form().data.get('url'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if kwargs.get('data'):
            url = kwargs.get('data').get('url')
        else:
            url = self.request.POST.get('url')
        if url is not None:
            url = normalize_url(url)

            kwargs['data'] = {'url': url}
        return kwargs
