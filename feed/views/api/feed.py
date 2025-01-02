from urllib.parse import urlparse, urlunparse

from django.db.models import Prefetch, Q
from django.http import QueryDict, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView

from feed.models import Feed, Collection, FeedItemAction, FeedItem
from feed.serializers import FeedSerializer, CollectionSerializer, FeedItemSerializer
from feed.tasks import parse_feed_info
from feed.utils.helpers import filter_by_feed_type
from feed.views.generic.feed_items_list import FeedFiltersMixin, GenericFeedItemListView
from feed.views.mixins import SidebarCacheCleaningMixin


class SubscriptionsListView(ListCreateAPIView):
    model = Feed
    serializer_class = FeedSerializer
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            subscribers=self.request.user
        ).prefetch_related(
            Prefetch(
                "collection_set",
                to_attr="collections",
                queryset=Collection.objects.filter(user=self.request.user),
            )
        )


class CollectionListView(ListCreateAPIView):
    model = Collection
    serializer_class = CollectionSerializer
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "feeds", queryset=Feed.objects.filter(subscribers=self.request.user)
            )
        )


class FeedListView(ListAPIView):
    model = FeedItem
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        queryset = (
            self.model.objects.filter(feed__subscribers=self.request.user)
            .prefetch_related("feed")
            .prefetch_related("actions")
        )

        queryset = self.apply_type_filters(queryset)
        queryset = self.apply_exclude_filters(queryset)
        queryset = self.apply_search_filter(queryset)
        return queryset

    def apply_exclude_filters(self, queryset):
        exclude_list = self.request.GET.getlist("exclude", default=[])

        for exclude in exclude_list:
            if "viewed" in exclude:
                queryset = queryset.exclude(
                    Q(actions__user=self.request.user),
                    Q(actions__type=FeedItemAction.Type.VIEW),
                )

            if "not_interesting" in exclude:
                queryset = queryset.exclude(
                    Q(actions__user=self.request.user),
                    Q(actions__type=FeedItemAction.Type.DISLIKE),
                )

            if "paid" in exclude:
                queryset = queryset.exclude(has_paid_content=True)

        return queryset

    def apply_type_filters(self, queryset):
        match self.request.GET.get("type"):
            case "favorite":
                return queryset.filter(
                    Q(actions__user=self.request.user),
                    Q(actions__type=FeedItemAction.Type.LIKE),
                )
            case "article":
                return filter_by_feed_type(queryset, "articles")
            case "podcast":
                return filter_by_feed_type(queryset, "podcasts")
            case "video":
                return filter_by_feed_type(queryset, "videos")
            case _:
                return queryset

    def apply_search_filter(self, queryset):
        if self.request.GET.get("search") is None:
            return queryset
        return queryset.filter(
            Q(title__icontains=self.request.GET.get("search"))
            | Q(description__icontains=self.request.GET.get("search"))
        )


class CollectionFeedListView(FeedListView):
    def get_queryset(self):
        return super().get_queryset().filter(feed__collection=self.kwargs.get("pk"))


class SubscriptionsFeedListView(FeedListView):
    def get_queryset(self):
        return super().get_queryset().filter(feed=self.kwargs.get("pk"))


class FullFeedList(GenericFeedItemListView):
    template_name = "blocks/feed/list.html"
    feet_item_url_name = "feed_detail"

    def get_feed_item_url_name(self):
        return self.feet_item_url_name

    def get_feed_url_name(self):
        return reverse("api_feed_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feet_item_url_name"] = self.get_feed_item_url_name()
        context["feed_url"] = self.get_feed_url_name()
        context["disliked"] = FeedItem.objects.filter(
            actions__user=self.request.user
        ).filter(actions__type=FeedItemAction.Type.DISLIKE)
        return context


class FeedItemUpdateView(UpdateAPIView):
    model = FeedItem
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class FeedItemActionView(View, SingleObjectMixin):
    model = FeedItem
    pk_url_kwarg = "feed_item_pk"
    http_method_names = ["post", "delete"]

    def post(self, request, *args, **kwargs):
        action = self.kwargs.get("action").upper()
        instance = self.get_object()
        action = FeedItemAction(
            type=FeedItemAction.Type[action],
            user=request.user,
            feed_item=instance,
        )
        action.save()
        instance.actions.add(action)
        instance.save()
        return JsonResponse({"success": True})

    def delete(self, request, *args, **kwargs):
        action = self.kwargs.get("action").upper()
        self.get_object().actions.filter(
            type=FeedItemAction.Type[action]
        ).first().delete()
        return JsonResponse({"success": True})


class UserFeedList(FullFeedList):
    http_method_names = ["get"]
    feed_type = None

    def get_feed_item_url_name(self):
        match self.feed_type:
            case "articles":
                return "feed_article_detail"
            case "podcasts":
                return "feed_podcast_detail"
            case "videos":
                return "feed_video_detail"
            case _:
                return "feed_detail"

    def get_feed_url_name(self):
        match self.feed_type:
            case "articles":
                return reverse("api_feed_articles")
            case "podcasts":
                return reverse("api_feed_podcasts")
            case "videos":
                return reverse("api_feed_videos")
            case _:
                return reverse("api_feed_list")

    def get_feed_type(self):
        return self.feed_type

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_type"] = self.get_feed_type()

        return context

    def get_queryset(self):
        feed_type = self.get_feed_type()
        queryset = super().get_queryset()
        if feed_type:
            queryset = filter_by_feed_type(queryset, feed_type)
        return queryset.filter(feed__subscribers=self.request.user)


class Favorites(UserFeedList):
    http_method_names = ["get"]
    available_filters = ["paid"]

    def get_feed_url_name(self):
        return reverse("api_feed_favorites")

    def get_feed_item_url_name(self):
        return "favorites_detail"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                actions__user=self.request.user, actions__type=FeedItemAction.Type.LIKE
            )
            .order_by("-actions__performed_at")
        )


class CollectionFeed(UserFeedList):
    http_method_names = ["get"]

    def get_feed_url_name(self):
        return reverse(
            "api_collection_feed",
            kwargs={"collection_id": self.kwargs.get("collection_id")},
        )

    def get_queryset(self):
        collection = Collection.objects.get(pk=self.kwargs.get("collection_id"))
        return super().get_queryset().filter(feed__collection=collection)


class FeedItemListView(FullFeedList):
    http_method_names = ["get"]
    feet_item_url_name = "subscription_detail"

    def get_feed_url_name(self):
        return reverse(
            "api_feed_feed_list", kwargs={"feed_id": self.kwargs.get("feed_id")}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_id"] = self.kwargs.get("feed_id")
        context["feed"] = Feed.objects.get(id=context["feed_id"])
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        feed_id = self.kwargs.get("feed_id")
        return queryset.filter(feed__id=feed_id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "RefreshFeedDescription"
        return response


class FeedFilters(TemplateView, FeedFiltersMixin):
    http_method_names = ["post"]
    template_name = "blocks/feed/filters.html"

    def post(self, request, *args, **kwargs):
        url = urlparse(request.headers.get("Referer"))
        query_dict = QueryDict(url.query, mutable=True)
        query_dict.setlist("filter", self.request.POST.getlist("filter"))
        url = url._replace(query=query_dict.urlencode())
        url = urlunparse(url)
        response = super().get(request, *args, **kwargs)
        response.headers["HX-Push-Url"] = url
        return response


class FeedTypes(TemplateView, ContextMixin):
    http_method_names = ["post"]
    template_name = "blocks/feed/types_selector.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_type"] = self.request.POST.get("feed_type")
        return context

    def post(self, request, *args, **kwargs):
        url = urlparse(request.headers.get("Referer"))
        query_dict = QueryDict(url.query, mutable=True)
        feed_type = self.request.POST.getlist("feed_type")
        if "none" not in feed_type:
            query_dict.setlist("feed_type", feed_type)
        else:
            query_dict.pop("feed_type")

        url = url._replace(query=query_dict.urlencode())
        url = urlunparse(url)
        response = super().get(request, *args, **kwargs)
        response.headers["HX-Redirect"] = url
        return response


class FeedUnsubscribe(DetailView, SidebarCacheCleaningMixin):
    http_method_names = ["post"]
    template_name = "blocks/feed/subscription.html"
    model = Feed
    pk_url_kwarg = "feed_id"

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        match action:
            case "unsubscribe":
                self.unsubscribe(request, *args, **kwargs)
            case "subscribe":
                self.subscribe(request, *args, **kwargs)

        self.clean_sidebar_feeds_cache()

        response = super().get(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "RefreshFeed, RefreshFeedList"
        return response

    def subscribe(self, request, *args, **kwargs):
        feed_id = kwargs.get("feed_id")
        feed = Feed.objects.get(pk=feed_id)
        feed.subscribers.add(request.user)
        feed.save()

    def unsubscribe(self, request, *args, **kwargs):
        feed_id = kwargs.get("feed_id")
        feed = Feed.objects.get(pk=feed_id)
        feed.subscribers.remove(request.user)
        feed.save()


class ParsingStatus(TemplateView):
    http_method_names = ["post"]

    def get_parsing_task(self):
        task_id = self.request.POST.get("task_id")
        async_result = parse_feed_info.AsyncResult(task_id)
        return async_result

    def get_parsing_result(self):
        task_result = self.get_parsing_task()
        if task_result.status == "PENDING" or task_result.status == "FAILURE":
            return []

        feed_ids = task_result.get()
        return Feed.objects.filter(id__in=feed_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_id"] = self.request.POST.get("task_id")
        context["result"] = self.get_parsing_result()
        return context

    def get_template_names(self):
        task = self.get_parsing_task()
        if task.status == "PENDING":
            return "blocks/feed/parsing_progress.html"
        if task.status == "FAILURE":
            return "blocks/feed/parsing_failed.html"

        task_result = self.get_parsing_result()

        if len(task_result) == 0:
            return "blocks/feed/parsing_empty.html"

        return "blocks/feed/parsing_done.html"

    def get_response_http_status(self):
        task_result = self.get_parsing_task()
        if task_result.status == "PENDING":
            return 200
        return 286

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        status = self.get_response_http_status()
        return self.render_to_response(context, status=status)
