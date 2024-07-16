from enum import Enum
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin

from django import forms
from feed.models import Feed
from articulo import Articulo
import feedparser

from feed.utils.helpers import get_url_content_type


class FeedContentTypes(Enum):
    TEXT_HTML = 'text/html'
    TEXT_XML = 'text/xml'
    APPLICATION_XML = 'application/xml'
    APPLICATION_XML_RSS = 'application/rss+xml'


class FeedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        if data is not None:
            url = kwargs.get('data').get('url')
            self.content_type = get_url_content_type(url)
            if self.content_type == FeedContentTypes.TEXT_HTML.value:
                self.articulo = Articulo(url)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.is_valid():
            base_url = self.cleaned_data['url']

            match self.content_type:
                case FeedContentTypes.TEXT_HTML:
                    self.parse_html(base_url)
                case FeedContentTypes.TEXT_XML.value \
                     | FeedContentTypes.APPLICATION_XML.value \
                     | FeedContentTypes.APPLICATION_XML_RSS.value:
                    self.parse_xml(base_url)
                case _:
                    print('Unsupported content type')

        return super().save(commit=commit)

    def clean(self):
        try:
            # Assuming that URL is valid and resolved.
            match self.content_type:
                case FeedContentTypes.TEXT_HTML:
                    # TODO Validate if:
                    #   - RSS link is reachable
                    if self.articulo.rss is None:
                        self.add_error('url', 'This URL could not be parsed.')
                case FeedContentTypes.TEXT_XML.value \
                     | FeedContentTypes.APPLICATION_XML.value \
                     | FeedContentTypes.APPLICATION_XML_RSS.value:
                    pass
                case _:
                    self.add_error('url', 'This URL could not be parsed.')
        except HTTPError:
            # Assuming that URL is valid, but we have an HTTP error in response.
            self.add_error('url', 'Something went wrong while parsing the URL. Try again later.')
        except URLError:
            # Assuming that URL is invalid or cannot be resolved.
            self.add_error('url', 'This URL could not be parsed.')

        return super().clean()

    def parse_xml(self, base_url):
        info = feedparser.parse(self.cleaned_data['url'])

        self.instance.title = info.feed.title
        self.instance.description = info.feed.description
        self.instance.icon = info.feed.image.href
        self.instance.rss_url = base_url
        self.instance.url = info.feed.link

    def parse_html(self, base_url):
        if self.articulo is None:
            return

        rss = self.articulo.rss
        rss = urljoin(base_url, rss)
        info = feedparser.parse(rss)

        self.instance.title = info.feed.get('title')
        self.instance.description = info.feed.get('description') or self.articulo.description
        self.instance.rss_url = rss
        self.instance.icon = info.feed.image.get('href') if info.feed.get('image') else self.articulo.icon

    class Meta:
        model = Feed
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Regular URL or RSS URL'}),
        }
