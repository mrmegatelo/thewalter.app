import feedparser
from articulo import Articulo
from django.db.models import Q
from django.views.generic import CreateView
from django.utils.translation import gettext_noop as _

from feed.forms import FeedForm
from feed.models import Feed
from feed.utils.enums import FeedContentTypes
from feed.utils.feed_parsers import RSSFeedParser, HTMLFeedParser
from feed.utils.feed_validators import HTMLLinkValidator, RSSLinkValidator
from feed.utils.helpers import normalize_url, get_url_content_type
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
            articulo = self.get_articulo_instance(url)
            try:
                existing_feed = Feed.objects.get(Q(url=url) | Q(rss_url=url))
                kwargs['instance'] = existing_feed
            except Feed.DoesNotExist:
                print('no feed found')

            kwargs['data'] = {'url': url}
            kwargs['feed_parser'] = self.get_form_parser(url, articulo)
            kwargs['validator'] = self.get_form_validator(url, articulo)
        return kwargs

    def get_form_parser(self, url, articulo):
        content_type = get_url_content_type(url)
        if content_type == FeedContentTypes.TEXT_HTML.value:
            return HTMLFeedParser(articulo)
        return RSSFeedParser(articulo)

    def get_form_validator(self, url, articulo):
        content_type = get_url_content_type(url)
        match content_type:
            case FeedContentTypes.TEXT_HTML.value:
                return HTMLLinkValidator(articulo)
            case FeedContentTypes.TEXT_XML.value \
                 | FeedContentTypes.APPLICATION_XML.value \
                 | FeedContentTypes.APPLICATION_XML_RSS.value \
                 | FeedContentTypes.APPLICATION_XML_ATOM.value:
                return RSSLinkValidator(articulo)

    def get_articulo_instance(self, url):
        content_type = get_url_content_type(url)
        if content_type == FeedContentTypes.TEXT_HTML.value:
            return Articulo(url)
        parsed = feedparser.parse(url)
        return Articulo(parsed.feed.get('link') or parsed.feed.get('href'))
