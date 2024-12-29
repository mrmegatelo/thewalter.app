from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from feed.models import Feed, Collection, FeedItem


class FeedSerializer(serializers.ModelSerializer):
    collections = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ["id", "title", "url", "description", "icon", "slug", "collections"]


class CollectionSerializer(serializers.ModelSerializer):
    feeds = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "slug", "feeds"]


class FeedItemSerializer(serializers.ModelSerializer):
    feed = PrimaryKeyRelatedField(read_only=True)

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
            "feed"
        ]