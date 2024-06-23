from feed.views.mixins import ProtectedViewMixin
from feed.views.feed.generic_feed_items_list import GenericFeedItemListView


class FeedItemsListView(ProtectedViewMixin, GenericFeedItemListView):
    http_method_names = ['get', 'post']
    def get_template_names(self):
        if self.request.method == 'POST' or self.request.headers.get('Hx-Request'):
            return ['blocks/feed/list.html']
        return ['feed/index.html']
