from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    collections = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ['title', 'url', 'description', 'icon', 'slug', 'collections']