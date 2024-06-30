from django import forms
from django.forms.widgets import HiddenInput
from feed.models import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['url', 'rss_url', 'title', 'description', 'created_by']
        widgets = {
            'created_by': HiddenInput()
        }
