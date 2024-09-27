from django.views.generic import ListView

from feed.models import Feed, FeedItem
from feed.utils.helpers import filter_by_attachments_type
from feed.views.generic.feed_items_list import FeedFiltersMixin


class FeedList(FeedFiltersMixin, ListView):
    template_name = 'feed/index.html'
    model = Feed

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ServiceFeedList(FeedList):
    template_name = 'feed/service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_id'] = self.kwargs.get('feed_id')

        return context

    def get_queryset(self):
        feed_id = self.kwargs.get('feed_id')
        queryset = super().get_queryset()

        if feed_id is not None:
            filtered_feed = filter_by_attachments_type(FeedItem.objects, feed_id).values_list('id', flat=True).distinct()
            return queryset.filter(feed_items__in=filtered_feed).distinct()
        return queryset
