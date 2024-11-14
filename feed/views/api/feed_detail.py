from django.views.generic import DetailView

from feed.models import FeedItem


class FeedDetail(DetailView):
    http_method_names = ['get']
    model = FeedItem

    def get_template_names(self):
        match self.object.type():
            case 'audio':
                return 'blocks/feed/detail/podcast.html'
            case 'video':
                return 'blocks/feed/detail/video.html'
            case _:
                return 'blocks/feed/detail/base.html'