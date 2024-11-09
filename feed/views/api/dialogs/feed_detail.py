from django.views.generic import DetailView

from feed.models import FeedItem
from feed.views.api.dialogs.generic import GenericDialog


class FeedDetail(DetailView, GenericDialog):
    http_method_names = ['get']
    dialog_position = 'bottom'
    dialog_id = 'feed_detail'
    model = FeedItem

    def get_template_names(self):
        match self.object.type():
            case 'audio':
                return 'dialogs/feed/detail/podcast.html'
            case 'video':
                return 'dialogs/feed/detail/video.html'
            case _:
                return 'dialogs/feed/detail/base.html'