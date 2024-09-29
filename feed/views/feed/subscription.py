from feed.views.feed.feed_items_list import FeedList


class Subscription(FeedList):
    template_name = 'feed/feed_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed'] = super().get_queryset().get(slug=self.kwargs.get('slug'))
        return context
