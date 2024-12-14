from django.urls import reverse

from feed.models import Collection
from feed.views.collection import CollectionCreate


class CollectionUpdateView(CollectionCreate):

    template_name = "forms/collection/update.html"

    def get_success_url(self):
        if self.request.headers.get("Hx-Request"):
            return reverse("api_dialog_hide")
        return reverse("collection_update", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = Collection.objects.get(slug=self.kwargs["slug"]).id
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = Collection.objects.get(slug=self.kwargs["slug"])
        return kwargs
