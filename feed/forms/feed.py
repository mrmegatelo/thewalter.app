from django import forms


class FeedForm(forms.Form):
    url = forms.URLField(label='')
