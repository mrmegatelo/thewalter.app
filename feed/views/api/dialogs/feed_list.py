from feed.models import FeedItem
from feed.utils.helpers import filter_by_attachments_type
from feed.views.feed.feed_items_list import FeedList


class FeedListDialog(FeedList):
    http_method_names = ['get']
    template_name = 'dialogs/feed/feed_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['dialog_id'] = 'feed_list'

        return context_data

    def get_queryset(self):
        feed_id = self.request.GET.get('feed_id')
        queryset = super().get_queryset()

        if feed_id is not None:
            filtered_feed = filter_by_attachments_type(FeedItem.objects, feed_id).values_list('id', flat=True).distinct()
            return queryset.filter(feed_items__in=filtered_feed).distinct()
        return queryset