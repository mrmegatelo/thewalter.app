from django.forms import HiddenInput, TextInput, CheckboxSelectMultiple
from django.forms.models import ModelForm

from feed.models import Collection


class CollectionForm(ModelForm):
    class Meta:
        fields = ["title", "feeds", "user"]
        model = Collection
        labels = {
            "title": "",
            "feeds": "Choose feeds:",
        }
        widgets = {
            "user": HiddenInput,
            "title": TextInput(),
            "feeds": CheckboxSelectMultiple(attrs={"label": ""}),
        }
