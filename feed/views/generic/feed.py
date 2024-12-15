from django.db.models import Prefetch
from django.views.generic import ListView

from feed.models import Collection, Feed
from feed.views.mixins import FeedFiltersMixin


class GenericFeedView(FeedFiltersMixin, ListView):
    feet_item_url_name = "feed_detail"
    feed_type = None
    model = Feed

    def get_template_names(self):
        if self.request.headers.get("Hx-Request") == "true":
            return self.get_loader_template_names()
        return self.get_regular_template_names()

    def get_regular_template_names(self):
        return "feed/index.html"

    def get_loader_template_names(self):
        return "blocks/feed/loaders/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_id"] = self.kwargs.get("feed_id")
        context["feed_item_id"] = self.kwargs.get("feed_item_id")
        context["feed_type"] = self.request.GET.get("feed_type")
        context["feed_item_url_name"] = self.feet_item_url_name
        context["collections"] = Collection.objects.filter(
            user=self.request.user
        ).prefetch_related(
            Prefetch(
                "feeds",
                to_attr="feeds_list",
                queryset=Feed.objects.filter(subscribers=self.request.user),
            )
        )

        if "item_pk" in self.kwargs:
            pk = self.kwargs.get("item_pk")
            context["feed_item_pk"] = pk
        return context

    def get_queryset(self):
        return super().get_queryset().filter(subscribers=self.request.user)
