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
    APPLICATION_XML_ATOM = 'application/atom+xml'


class FeedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        if data is not None:
            url = kwargs.get('data').get('url')
            self.content_type = get_url_content_type(url)
            if self.content_type == FeedContentTypes.TEXT_HTML.value:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }
                self.articulo = Articulo(url, http_headers=headers)
        else:
            self.content_type = FeedContentTypes.APPLICATION_XML.value
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.is_valid():
            base_url = self.data.get('url')

            match self.content_type:
                case FeedContentTypes.TEXT_HTML.value:
                    self.parse_html(base_url)
                case FeedContentTypes.TEXT_XML.value \
                     | FeedContentTypes.APPLICATION_XML.value \
                     | FeedContentTypes.APPLICATION_XML_RSS.value \
                     | FeedContentTypes.APPLICATION_XML_ATOM.value:
                    self.parse_xml(base_url)
                case _:
                    print('Unsupported content type')
        print('saving the model')
        return super().save(commit=commit)

    def full_clean(self):
        super().full_clean()
        try:
            # Assuming that URL is valid and resolved.
            match self.content_type:
                case FeedContentTypes.TEXT_HTML.value:
                    # TODO Validate if:
                    #   - RSS link is reachable
                    #   - if all the model fields are valid
                    if self.articulo.rss is None:
                        self.add_error('url', 'This link has no feed.')
                case FeedContentTypes.TEXT_XML.value \
                     | FeedContentTypes.APPLICATION_XML.value \
                     | FeedContentTypes.APPLICATION_XML_RSS.value \
                     | FeedContentTypes.APPLICATION_XML_ATOM.value:
                    pass
                case _:
                    self.add_error('url', 'This URL could not be parsed.')
        except HTTPError:
            # Assuming that URL is valid, but we have an HTTP error in response.
            self.add_error('url', 'Something went wrong while parsing the URL. Try again later.')
        except URLError:
            # Assuming that URL is invalid or cannot be resolved.
            self.add_error('url', 'This URL could not be parsed.')

    def parse_xml(self, base_url):
        info = feedparser.parse(self.cleaned_data['url'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        articulo = Articulo(info.feed.link, http_headers=headers)

        self.instance.title = info.feed.title
        self.instance.description = info.feed.description
        self.instance.rss_url = base_url
        self.instance.url = info.feed.link
        if info.feed.get('image') is not None:
            self.instance.icon = info.feed.image.href
        elif info.feed.get('icon') is not None:
            self.instance.icon = info.feed.icon
        elif articulo.icon is not None:
            self.instance.icon = articulo.icon

    def parse_html(self, base_url):
        if self.articulo is None:
            return

        rss = self.articulo.rss
        rss = urljoin(base_url, rss)
        info = feedparser.parse(rss)

        self.instance.title = info.feed.get('title')
        self.instance.description = info.feed.get('description') or self.articulo.description
        self.instance.rss_url = rss
        if info.feed.get('image') is not None:
            self.instance.icon = info.feed.image.href
        elif info.feed.get('icon') is not None:
            self.instance.icon = info.feed.icon
        else:
            self.instance.icon = self.articulo.icon

    class Meta:
        model = Feed
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Regular URL or RSS URL'}),
        }
