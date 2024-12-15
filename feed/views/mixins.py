from django.views.generic.base import ContextMixin, View
from django.utils.translation import gettext_noop as _

from feed.models import Feed, FeedItem
from feed.utils.helpers import filter_by_feed_type


class PageMetaMixin(ContextMixin):
    title = "thewalter.app"
    description = _("The only feed you need.")
    cover = "feed/img/cover.jpg"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title,
                "description": self.description,
                "cover": self.cover,
            }
        )
        return context


class FeedFiltersMixin(ContextMixin, View):
    applied_filters = {"not_interesting": True, "viewed": True}
    available_filters = ["not_interesting", "viewed", "paid"]

    def setup(self, request, *args, **kwargs):
        filters = self.init_filters(request)
        if filters:
            new_filters = dict()
            for name in filters:
                new_filters[name] = True
            self.applied_filters = new_filters
        return super().setup(request, *args, **kwargs)

    def init_filters(self, request):
        request_params = request.GET if request.method == "GET" else request.POST
        return request_params.getlist("filter")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applied_filters"] = self.applied_filters
        context["available_filters"] = self.available_filters
        context["reload_filters"] = self.request.headers.get("HX-Request") == "true"
        return context


class FeedContextMixin(ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feed_type = self.request.GET.get("feed_type")
        context["feed_id"] = self.kwargs.get("feed_id")
        context["feed_type"] = feed_type
        context["feed_list"] = Feed.objects.filter(subscribers=self.request.user)

        # TODO: this is a suboptimal way to retrieve the feeds by their feed item types
        #  Need to find a better way to do it.
        if context["feed_type"] is not None:
            filtered_feed = (
                filter_by_feed_type(FeedItem.objects, feed_type)
                .values_list("id", flat=True)
                .distinct()
            )
            context["feed_list"] = (
                context["feed_list"].filter(feed_items__in=filtered_feed).distinct()
            )

        return context
