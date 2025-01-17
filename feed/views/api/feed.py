from django.contrib.auth.models import User
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Feed, Collection, FeedItemAction, FeedItem
from feed.serializers import FeedSerializer, CollectionSerializer, FeedItemSerializer
from feed.tasks import parse_feed_info
from feed.utils.helpers import filter_by_feed_type


class SubscriptionsListView(ListCreateAPIView):
    model = Feed
    serializer_class = FeedSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = self.model.objects.filter(subscribers=self.request.user)
        return self.get_prefetched_queryset(queryset)

    def create(self, request, *args, **kwargs):
        serializer_data = self.get_serializer_data(request)
        serializer = self.get_serializer(serializer_data, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_serializer_data(self, request):
        url = request.data.get("url")
        parsed_feeds_ids = parse_feed_info.delay(url).get()
        parsed_feeds = self.model.objects.filter(id__in=parsed_feeds_ids)
        return self.get_prefetched_queryset(parsed_feeds)

    def get_prefetched_queryset(self, queryset):
        return queryset.prefetch_related(
            Prefetch(
                "collections",
                queryset=Collection.objects.filter(user=self.request.user),
            )
        ).prefetch_related(
            Prefetch(
                "subscribers",
                to_attr="is_subscribed",
                queryset=User.objects.filter(pk=self.request.user.pk),
            )
        )


class CollectionListView(ListCreateAPIView):
    model = Collection
    serializer_class = CollectionSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            self.model.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "feeds", queryset=Feed.objects.filter(subscribers=self.request.user)
                )
            )
            .prefetch_related("user")
        )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CollectionUpdateView(UpdateAPIView):
    model = Collection
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return (
            self.model.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "feeds", queryset=Feed.objects.filter(subscribers=self.request.user)
                )
            )
            .prefetch_related("user")
        )


class FeedListView(ListAPIView):
    model = FeedItem
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        queryset = (
            self.model.objects.filter(feed__subscribers=self.request.user)
            .prefetch_related("feed")
            .prefetch_related("actions")
            .prefetch_related("attachments")
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
                ).order_by("-actions__performed_at")
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
        return super().get_queryset().filter(feed__collections=self.kwargs.get("pk"))


class SubscriptionsFeedListView(FeedListView):
    def get_queryset(self):
        return super().get_queryset().filter(feed=self.kwargs.get("pk"))


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


class Subscription(APIView, SingleObjectMixin):
    model = Feed
    http_method_names = ["post", "delete"]
    serializer_class = FeedSerializer

    def get_queryset(self):
        return self.get_prefetched_queryset(super().get_queryset())

    def post(self, request, *args, **kwargs):
        feed = self.get_object()
        feed.subscribers.add(request.user)
        feed.is_subscribed.append(request.user)
        feed.save()
        return Response(
            self.serializer_class(feed).data
        )

    def delete(self, request, *args, **kwargs):
        feed = self.get_object()
        feed.subscribers.remove(request.user)
        feed.save()
        return JsonResponse({"success": True})

    def get_prefetched_queryset(self, queryset):
        return queryset.prefetch_related(
            Prefetch(
                "collections",
                queryset=Collection.objects.filter(user=self.request.user),
            )
        ).prefetch_related(
            Prefetch(
                "subscribers",
                to_attr="is_subscribed",
                queryset=User.objects.filter(pk=self.request.user.pk),
            )
        )