from feed.views.feed import FeedView


class Favorites(FeedView):
    template_name = 'feed/favorites.html'