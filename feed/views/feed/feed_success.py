from django.db.models import Q
from django.utils.translation import gettext_noop as _

from feed.models import Feed
from feed.views.feed import FeedCreate


class Created(FeedCreate):
    template_name = 'feed/success.html'
    title = _('My feed')

    def get_context_data(self, **kwargs):
        url = self.request.GET.get('url')
        context = super().get_context_data(**kwargs)

        feed_list = Feed.objects.filter(Q(url=url) | Q(rss_url=url))
        context['result'] = feed_list

        return context
