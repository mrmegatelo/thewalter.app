from feed.views.feed.feed import FeedView


class Subscription(FeedView):

    def get_regular_template_names(self):
        return 'feed/subscription.html'

    def get_loader_template_names(self):
        return 'blocks/feed/loaders/subscription.html'
