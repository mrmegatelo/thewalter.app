from django.db.models import Q
from django.views.generic import CreateView
from django.utils.translation import gettext_noop as _

from feed.forms import FeedForm
from feed.models import Feed
from feed.utils.helpers import normalize_url
from feed.views.mixins import PageMetaMixin


class Create(CreateView, PageMetaMixin):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed/new/success/'
    title = _('My feed')

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object.subscribers.add(self.request.user)
        return result

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        url = self.request.POST.get('url')
        if url is not None:
            url = normalize_url(url)
            try:
                existing_feed = Feed.objects.get(Q(url=url) | Q(rss_url=url))
                kwargs['instance'] = existing_feed
                kwargs['data'] = {'url': url}
                return kwargs
            except Feed.DoesNotExist:
                print('no feed found')

        return kwargs
