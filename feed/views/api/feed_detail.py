from urllib.parse import urlparse

from django.http import QueryDict
from django.views.generic import DetailView

from feed.models import FeedItem


class FeedDetail(DetailView):
    http_method_names = ['get']
    model = FeedItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked'] = self.request.user.servicefeed_set.filter(type='liked').first()
        context['disliked'] = self.request.user.servicefeed_set.filter(type='disliked').first()
        return context

    def get_template_names(self):
        match self.object.type():
            case 'audio':
                return 'blocks/feed/detail/podcast.html'
            case 'video':
                return 'blocks/feed/detail/video.html'
            case _:
                return 'blocks/feed/detail/base.html'

class FeedItemActions(FeedDetail):
    http_method_names = ["post"]

    def get_feed_type(self):
        parsed_url = urlparse(self.request.headers.get("hx-current-url"))
        query = QueryDict(parsed_url.query, mutable=False)
        return query.get("feed_type")

    def init_filters(self, request):
        url = urlparse(request.headers.get("hx-current-url"))
        query_dict = QueryDict(url.query)
        return query_dict.getlist("filter")

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")

        match action:
            case "toggle_interesting":
                self.toggle_interesting(request, *args, **kwargs)
            case "toggle_liked":
                self.toggle_liked(request, *args, **kwargs)
            case _:
                pass
        response = super().get(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "RefreshFeed"
        return response

    def toggle_interesting(self, request, *args, **kwargs):
        feed_item = self.get_object()
        user = request.user

        disliked_qs = user.servicefeed_set.filter(type="disliked").first().feed_items
        if disliked_qs.contains(feed_item):
            disliked_qs.remove(feed_item)
        else:
            disliked_qs.add(feed_item)
        return feed_item

    def toggle_liked(self, request, *args, **kwargs):
        feed_item = self.get_object()
        user = request.user

        liked_qs = user.servicefeed_set.filter(type="liked").first().feed_items

        if liked_qs.contains(feed_item):
            liked_qs.remove(feed_item)
        else:
            liked_qs.add(feed_item)

        return feed_item