from django import forms
from feed.models import Feed

from feed.utils.feed_parsers import AbstractFeedParser
from feed.utils.feed_validators import AbstractValidator
from feed.utils.helpers import get_url_content_type


class FeedForm(forms.ModelForm):
    feed_parser: AbstractFeedParser
    validator: AbstractValidator

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')

        if data is not None:
            url = data.get('url')
            self.content_type = get_url_content_type(url)
            self.feed_parser = kwargs.pop('feed_parser')
            self.validator = kwargs.pop('validator')

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.is_valid():
            base_url = self.data.get('url')
            self.parse(base_url)
        return super().save(commit=commit)

    def full_clean(self):
        super().full_clean()
        if not self.is_bound:
            return

        if hasattr(self, 'validator') and self.validator is not None:
            error = self.validator.validate(self.data.get('url'))

            if error is not None:
                self.add_error('url', error)
        else:
            self.add_error('url', 'This URL could not be parsed.')

    def parse(self, url):
        feed_meta = self.feed_parser.parse(url)
        self.instance.title = feed_meta.title
        self.instance.description = feed_meta.description
        self.instance.rss_url = feed_meta.rss_url
        self.instance.url = feed_meta.url
        self.instance.icon = feed_meta.icon_url

    class Meta:
        model = Feed
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Regular URL or RSS URL'}),
        }
