from django.views.generic import ListView

from feed.models import Feed
from feed.views.generic.feed_items_list import FeedFiltersMixin


class FeedView(FeedFiltersMixin, ListView):
    feet_item_url_name = "feed_detail"
    feed_type = None
    model = Feed

    def get_template_names(self):
        if self.request.headers.get("Hx-Request") == "true":
            return self.get_loader_template_names()
        return self.get_regular_template_names()

    def get_regular_template_names(self):
        match self.feed_type:
            case "articles":
                return "feed/articles.html"
            case "podcasts":
                return "feed/podcasts.html"
            case "videos":
                return "feed/videos.html"
            case _:
                return "feed/index.html"

    def get_loader_template_names(self):
        match self.feed_type:
            case "articles":
                return "blocks/feed/loaders/articles.html"
            case "podcasts":
                return "blocks/feed/loaders/podcasts.html"
            case "videos":
                return "blocks/feed/loaders/videos.html"
            case _:
                return "blocks/feed/loaders/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_id"] = self.kwargs.get("feed_id")
        context["feed_item_id"] = self.kwargs.get("feed_item_id")
        context["feed_type"] = self.request.GET.get("feed_type")
        context["feed_item_url_name"] = self.feet_item_url_name

        if "slug" in self.kwargs:
            slug = self.kwargs.get("slug")
            context["feed"] = super().get_queryset().get(slug=slug)

        if "item_pk" in self.kwargs:
            pass
            pk = self.kwargs.get("item_pk")
            context["feed_item_pk"] = pk
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(subscribers=self.request.user)
        return queryset
