from feed.views.feed.feed_items_list import FeedList


class FeedListDialog(FeedList):
    http_method_names = ['post']
    template_name = 'dialogs/feed/feed_list.html'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['dialog_id'] = 'feed_list'

        return context_data