from feed.views.generic.feed_items_list import GenericFeedItemListView


class FeedItemsListView(GenericFeedItemListView):
    template_name = 'feed/index.html'


class ServiceFeedItemsListView(FeedItemsListView):
    template_name = 'feed/service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_id'] = self.kwargs.get('feed_id')

        return context

    def get_queryset(self):
        feed_id = self.kwargs.get('feed_id')
        queryset = super().get_queryset()
        match feed_id:
            case 'podcasts':
                return queryset.filter(attachments__type='audio')
            case _:
                return queryset
