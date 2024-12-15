from urllib.parse import urlparse

from django.urls import resolve
from django.views.generic import DetailView
from feed.models import FeedItem, ServiceFeed
from feed.utils.helpers import filter_by_feed_type


class FeedItemDetailView(DetailView):
    http_method_names = ["get"]
    model = FeedItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked"] = self.request.user.servicefeed_set.filter(
            type="liked"
        ).first()
        context["disliked"] = self.request.user.servicefeed_set.filter(
            type="disliked"
        ).first()
        return context

    def get_template_names(self):
        match self.object.type:
            case "audio":
                return "blocks/feed/detail/podcast.html"
            case "video":
                return "blocks/feed/detail/video.html"
            case _:
                return "blocks/feed/detail/base.html"


class FeedItemActions(FeedItemDetailView):
    http_method_names = ["post"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_list"] = True
        context["oob_value"] = self.get_oob_value()
        return context

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

    def get_oob_value(self):
        action = self.kwargs.get("action")
        match action:
            case "toggle_interesting":
                return self.get_interesting_action_oob_value()
            case _:
                return "true"

    def get_interesting_action_oob_value(self):
        feed_item = self.get_object()
        was_disliked = feed_item.service_feeds.filter(type="disliked").exists()

        if was_disliked:
            return f"delete:#feed_item_{feed_item.id}"

        qs = self.get_feed_items_queryset()
        next_feed_item = qs.filter(pub_date__lt=feed_item.pub_date).first()

        if next_feed_item:
            return f"beforebegin:#feed_item_{next_feed_item.id}"

        return "true"

    def get_feed_items_queryset(self):
        parsed_referrer = urlparse(self.request.headers.get("Referer"))
        resolved_url = resolve(parsed_referrer.path)

        if resolved_url.url_name == "subscription_detail":
            return self.get_object().feed.feed_items

        if resolved_url.url_name == "favorites_detail":
            return FeedItem.objects.filter(
                service_feeds__user=self.request.user
            ).filter(service_feeds__type=ServiceFeed.Type.LIKED)

        user_feed_items_qs = FeedItem.objects.filter(
            feed__subscribers=self.request.user
        )

        match resolved_url.url_name:
            case "feed_podcast_detail":
                return filter_by_feed_type(user_feed_items_qs, "podcasts")
            case "feed_video_detail":
                return filter_by_feed_type(user_feed_items_qs, "videos")
            case "feed_article_detail":
                return filter_by_feed_type(user_feed_items_qs, "articles")
            case _:
                return user_feed_items_qs
