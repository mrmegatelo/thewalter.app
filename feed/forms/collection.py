from django.forms import HiddenInput, TextInput
from django.forms.models import ModelForm

from feed.models import Collection


class CollectionForm(ModelForm):
    class Meta:
        fields = ["title", "user"]
        model = Collection
        labels = {"title": ""}
        widgets = {"user": HiddenInput, "title": TextInput(attrs={"label": ""})}
