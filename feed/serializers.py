from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from feed.models import Feed, Collection, FeedItem, FeedItemAction


class ExistenceCheckRelatedField(serializers.RelatedField):
    queryset = FeedItemAction.objects.all()

    def to_representation(self, instance):
        print("Is bool: ", isinstance(instance, list))
        if isinstance(instance, list):
            return len(instance) > 0
        return instance

    def to_internal_value(self, data):
        print(vars(self.context.get('request')))
        return data


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