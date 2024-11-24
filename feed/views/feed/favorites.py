from feed.views.feed import FeedView


class Favorites(FeedView):
    def get_template_names(self):
        return 'feed/favorites.html'