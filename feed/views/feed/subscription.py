from feed.views.feed.feed import FeedView


class Subscription(FeedView):
    template_name = 'feed/subscription.html'
