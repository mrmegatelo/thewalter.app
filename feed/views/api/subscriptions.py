from django.views.generic import ListView

from feed.models import Feed
from feed.views.mixins import FeedFiltersMixin


class SubscriptionsView(ListView, FeedFiltersMixin):
    model = Feed
    template_name = 'blocks/feed/feeds_full.html'
    context_object_name = 'feed_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(subscribers=self.request.user)