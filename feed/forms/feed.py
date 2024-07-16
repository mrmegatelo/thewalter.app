from urllib.error import HTTPError, URLError
from urllib.parse import urljoin

from django import forms
from feed.models import Feed
from articulo import Articulo
import feedparser

from feed.utils.helpers import get_url_content_type


class FeedForm(forms.ModelForm):

    def save(self, commit=True):
        print(self.is_valid())
        if self.is_valid():
            print('saving...')
            base_url = self.cleaned_data['url']
            content_type = get_url_content_type(base_url)

            match content_type:
                case 'text/html':
                    self.parse_html(base_url)
                case 'application/xml' | 'text/xml' | 'application/rss+xml':
                    self.parse_xml(base_url)
                case _:
                    print('Unsupported content type')

            return super().save(commit=commit)

    def clean(self):
        url = self.data.get('url')
        try:
            content_type = get_url_content_type(url)
            # Assuming that URL is valid and resolved.
            match content_type:
                case 'text/html':
                    # TODO Validate if:
                    #   - HTML has RSS link
                    #   - RSS link is reachable
                    pass
                case 'application/xml' | 'text/xml' | 'application/rss+xml':
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

        self.instance.title = info.feed.title
        self.instance.description = info.feed.description
        self.instance.icon = info.feed.image.href
        self.instance.rss_url = base_url
        self.instance.url = info.feed.link

    def parse_html(self, base_url):
        article = Articulo(base_url)
        rss = article.rss

        rss = urljoin(base_url, rss)
        info = feedparser.parse(rss)

        self.instance.title = info.feed.get('title')
        self.instance.description = info.feed.get('description') or article.description
        self.instance.rss_url = rss
        self.instance.icon = info.feed.image.get('href') if info.feed.get('image') else article.icon

    class Meta:
        model = Feed
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Regular URL or RSS URL'}),
        }
