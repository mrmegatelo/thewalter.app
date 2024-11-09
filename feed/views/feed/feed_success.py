from django.db.models import Q
from django.utils.translation import gettext_noop as _

from feed.models import Feed

from feed.utils.helpers import (
    get_articulo_instance,
    get_form_parser,
)
from feed.views.feed import FeedCreate


class Created(FeedCreate):
    template_name = 'feed/success.html'
    title = _('My feed')

    def get_initial(self):
        return {
            'url': self.request.GET.get('url')
        }

    def get_context_data(self, **kwargs):
        url = self.request.GET.get('url')
        context = super().get_context_data(**kwargs)

        feed_list  = Feed.objects.filter(Q(url__contains=url) | Q(rss_url__contains=url)).all()
        if feed_list.count() == 0:
            context["result"] = self.parse_and_save()
        else:
            context["result"] = feed_list
        return context


    def parse_and_save(self):
        url = self.request.GET.get('url')
        articulo = get_articulo_instance(url)
        parser = get_form_parser(url, articulo)
        feeds = []

        for link_meta in parser.parse(url):
            feed = Feed(
                title=link_meta.title,
                url=link_meta.url,
                description=link_meta.description,
                rss_url=link_meta.rss_url,
                icon=link_meta.icon_url,
            )
            feed.save()
            feeds.append(feed)
        return feeds