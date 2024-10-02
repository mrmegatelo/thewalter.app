from django.db.models import Q
from django.views.generic import CreateView
from django.utils.translation import gettext_noop as _

from feed.forms import FeedForm
from feed.models import Feed
from feed.utils.helpers import normalize_url, get_form_parser, get_articulo_instance, get_form_validator
from feed.views.mixins import PageMetaMixin, FeedContextMixin, FeedFiltersMixin


class FeedCreate(CreateView, PageMetaMixin, FeedContextMixin, FeedFiltersMixin):
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
            articulo = get_articulo_instance(url)
            try:
                existing_feed = Feed.objects.get(Q(url=url) | Q(rss_url=url))
                kwargs['instance'] = existing_feed
            except Feed.DoesNotExist:
                print('no feed found')

            kwargs['data'] = {'url': url}
            kwargs['feed_parser'] = get_form_parser(url, articulo)
            kwargs['validator'] = get_form_validator(url, articulo)
        return kwargs
