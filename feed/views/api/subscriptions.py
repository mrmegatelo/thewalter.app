from django.views.generic import ListView

from feed.models import Feed, Collection
from feed.views.mixins import FeedFiltersMixin


class SubscriptionsView(ListView, FeedFiltersMixin):
    model = Feed
    template_name = "blocks/feed/feeds_full.html"
    context_object_name = "feed_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections"] = Collection.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(subscribers=self.request.user)
            .filter(collection__isnull=True)
        )
