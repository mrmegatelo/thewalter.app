from django.views.generic import ListView

from feed.models import Feed, FeedItem
from feed.utils.helpers import filter_by_attachments_type
from feed.views.generic.feed_items_list import FeedFiltersMixin

class FeedView(FeedFiltersMixin, ListView):
    template_name = 'feed/index.html'
    feet_item_url_name = 'feed_detail'
    model = Feed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_id'] = self.kwargs.get('feed_id')
        context['feed_item_id'] = self.kwargs.get('feed_item_id')
        context['feed_type'] = self.request.GET.get('feed_type')
        context['feed_item_url_name'] = self.feet_item_url_name

        if 'slug' in self.kwargs:
            slug = self.kwargs.get('slug')
            context['feed'] = super().get_queryset().get(slug=slug)

        if 'item_pk' in self.kwargs:
            pass
            pk = self.kwargs.get('item_pk')
            context['feed_item_pk'] = pk
        return context

    def get_queryset(self):
        feed_type = self.request.GET.get('feed_type')
        queryset = super().get_queryset()
        queryset = queryset.filter(subscribers=self.request.user)
        if feed_type is not None:
            filtered_feed = filter_by_attachments_type(FeedItem.objects, feed_type).values_list('id',
                                                                                                flat=True).distinct()
            return queryset.filter(feed_items__in=filtered_feed).distinct()
        return queryset
