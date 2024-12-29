from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from feed.models import Feed, Collection


class FeedSerializer(serializers.ModelSerializer):
    collections = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ['id', 'title', 'url', 'description', 'icon', 'slug', 'collections']

class CollectionSerializer(serializers.ModelSerializer):
    feeds = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['title', 'slug', 'feeds']