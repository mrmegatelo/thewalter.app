from django.db.models import Q
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
            ).filter(Q(collection__isnull=True) | Q(collection__pk=self.instance.pk))

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
