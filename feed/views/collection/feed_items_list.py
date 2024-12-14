from feed.models import Collection
from feed.views.generic.feed import GenericFeedView


class CollectionFeedItemsListView(GenericFeedView):
    def get_regular_template_names(self):
        return "feed/collection.html"

    def get_loader_template_names(self):
        return "blocks/feed/loaders/collection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(slug=self.kwargs.get("slug"))
        return context
