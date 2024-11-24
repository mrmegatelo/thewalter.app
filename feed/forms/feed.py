from django import forms


class FeedForm(forms.Form):
    url = forms.URLField(label='', widget=forms.URLInput(attrs={'placeholder': 'Feed or Site URL'}))
