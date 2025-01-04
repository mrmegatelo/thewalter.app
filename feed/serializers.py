from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from feed.models import Feed, Collection, FeedItem


class ExistenceCheckRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        if isinstance(instance, list):
            return len(instance) > 0
        return instance


class FeedSerializer(serializers.ModelSerializer):
    collections = PrimaryKeyRelatedField(many=True, read_only=True)
    is_subscribed = ExistenceCheckRelatedField(read_only=True)

    class Meta:
        model = Feed
        fields = ["id", "title", "url", "description", "icon", "slug", "collections", "is_subscribed"]


class CollectionSerializer(serializers.ModelSerializer):
    feeds = PrimaryKeyRelatedField(many=True, queryset=Feed.objects.all())
    user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Collection
        fields = ["id", "title", "slug", "feeds", "user"]


class FeedItemSerializer(serializers.ModelSerializer):
    feed = PrimaryKeyRelatedField(read_only=True)
    actions = StringRelatedField(many=True)

    class Meta:
        model = FeedItem
        fields = [
            "id",
            "title",
            "description",
            "pub_date",
            "has_paid_content",
            "link",
            "preview",
            "feed",
            "actions",
        ]