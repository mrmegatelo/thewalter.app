from feed.views.feed.feed import FeedView


class Subscription(FeedView):

    def get_template_names(self):
        return 'feed/subscription.html'
