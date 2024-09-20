from django.views.generic import DetailView

from feed.models import Feed


class Subscription(DetailView):
    model = Feed

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)