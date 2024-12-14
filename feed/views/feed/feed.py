from feed.views.generic.feed import GenericFeedView


class FeedView(GenericFeedView):
    def get_regular_template_names(self):
        match self.feed_type:
            case "articles":
                return "feed/articles.html"
            case "podcasts":
                return "feed/podcasts.html"
            case "videos":
                return "feed/videos.html"
            case _:
                return super().get_regular_template_names()

    def get_loader_template_names(self):
        match self.feed_type:
            case "articles":
                return "blocks/feed/loaders/articles.html"
            case "podcasts":
                return "blocks/feed/loaders/podcasts.html"
            case "videos":
                return "blocks/feed/loaders/videos.html"
            case _:
                return super().get_loader_template_names()

    def get_queryset(self):
        return super().get_queryset().filter(collection__isnull=True)
