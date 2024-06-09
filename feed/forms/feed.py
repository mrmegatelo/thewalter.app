from django import forms
from feed.models import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['title', 'description', 'url', 'rss_url']
