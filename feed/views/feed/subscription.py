from django.views.generic import DetailView

from feed.models import Feed
from feed.views.feed.generic_feed_items_list import FeedFiltersMixin


class Subscription(DetailView, FeedFiltersMixin):
    model = Feed

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)