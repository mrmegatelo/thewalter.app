from feed.models import FeedItem
from feed.utils.helpers import filter_by_attachments_type
from feed.views.api.dialogs.generic import GenericDialog
from feed.views.feed.feed_list import FeedList


class FeedListDialog(FeedList, GenericDialog):
    http_method_names = ['get']
    template_name = 'dialogs/feed/feed_list.html'
    dialog_position = 'top'
    dialog_id = 'feed_list'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['feed_type'] = self.request.GET.get('feed_type')

        return context_data

    def get_queryset(self):
        feed_id = self.request.GET.get('feed_type')
        queryset = super().get_queryset()

        if feed_id is not None:
            filtered_feed = filter_by_attachments_type(FeedItem.objects, feed_id).values_list('id', flat=True).distinct()
            return queryset.filter(feed_items__in=filtered_feed).distinct()
        return queryset.filter(subscribers=self.request.user)