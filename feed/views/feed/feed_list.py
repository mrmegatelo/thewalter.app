from django.views.generic import ListView

from feed.models import Feed, FeedItem
from feed.utils.helpers import filter_by_attachments_type
from feed.views.generic.feed_items_list import FeedFiltersMixin


class FeedList(FeedFiltersMixin, ListView):
    template_name = 'feed/index.html'
    model = Feed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_id'] = self.kwargs.get('feed_id')
        context['feed_type'] = self.request.GET.get('feed_type')

        slug = self.kwargs.get('slug')

        if 'slug' in self.kwargs:
            context['feed'] = super().get_queryset().get(slug=slug)
        return context

    def get_queryset(self):
        feed_type = self.request.GET.get('feed_type')
        queryset = super().get_queryset()
        if feed_type is not None:
            filtered_feed = filter_by_attachments_type(FeedItem.objects, feed_type).values_list('id',
                                                                                              flat=True).distinct()
            return queryset.filter(feed_items__in=filtered_feed).distinct()
        return queryset
