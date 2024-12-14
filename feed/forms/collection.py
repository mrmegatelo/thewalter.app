from django.forms import HiddenInput, TextInput, CheckboxSelectMultiple
from django.forms.models import ModelForm

from feed.models import Collection, Feed


class CollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.get("initial").get("user")
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["feeds"].queryset = Feed.objects.filter(
                subscribers=user
            ).filter(collection__isnull=True)

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
