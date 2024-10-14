from feed.views.feed import FeedList


class Favorites(FeedList):
    template_name = 'feed/favorites.html'