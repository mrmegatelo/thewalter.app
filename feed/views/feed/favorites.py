from feed.views.feed import FeedView


class Favorites(FeedView):
    available_filters = ["paid"]

    def get_regular_template_names(self):
        return 'feed/favorites.html'

    def get_loader_template_names(self):
        return 'blocks/feed/loaders/favorites.html'