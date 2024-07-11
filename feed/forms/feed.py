from urllib.parse import urljoin

from django import forms
from feed.models import Feed
from articulo import Articulo


class FeedForm(forms.ModelForm):

    def save(self, commit=True):
        base_url = self.cleaned_data['url']
        article = Articulo(base_url)
        rss = article.rss
        self.instance.title = article.title
        self.instance.description = article.description
        self.instance.rss_url = urljoin(base_url, rss)
        self.instance.icon = article.icon
        return super().save(commit=commit)

    class Meta:
        model = Feed
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Regular URL or RSS URL'}),
        }
