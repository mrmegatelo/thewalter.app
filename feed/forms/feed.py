from django import forms
from django.forms.widgets import HiddenInput
from feed.models import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['title', 'description', 'url', 'rss_url', 'created_by']
        widgets = {
            'created_by': HiddenInput()
        }
