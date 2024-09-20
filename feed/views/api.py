from urllib.parse import urlparse, urlunparse

from django.core.paginator import InvalidPage
from django.http import QueryDict, Http404
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from feed.models import UserSettings
from feed.views.feed.generic_feed_items_list import GenericFeedItemListView, FeedFiltersMixin


class GenericApiFeedItemListView(GenericFeedItemListView):
    template_name = 'blocks/feed/list.html'

    def paginate_queryset(self, queryset, page_size):
        url = urlparse(self.request.headers.get('Referer'))
        """TODO: This is a dirty hack to get the page number from the referer. Fix it."""
        query_dict = QueryDict(url.query, mutable=True)
        page = query_dict.get('page') or 1

        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        try:
            page_number = int(page)
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _("Page is not “last”, nor can it be converted to an int.")
                )
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )


class FeedItemListView(GenericApiFeedItemListView):
    http_method_names = ['get']


class FeedFilters(TemplateView, FeedFiltersMixin):
    http_method_names = ['post']
    template_name = 'blocks/feed/filters.html'

    def post(self, request, *args, **kwargs):
        url = urlparse(request.headers.get('Referer'))
        query_dict = QueryDict(url.query, mutable=True)
        query_dict.setlist('filter', self.request.POST.getlist('filter'))
        url = url._replace(query=query_dict.urlencode())
        url = urlunparse(url)
        response = super().get(request, *args, **kwargs)
        response.headers['HX-Push-Url'] = url
        response.headers['HX-Trigger'] = 'loadFeedList'
        return response


class FeedItemActions(GenericApiFeedItemListView):
    http_method_names = ['post']

    def init_filters(self, request):
        url = urlparse(request.headers.get('Referer'))
        query_dict = QueryDict(url.query)
        return query_dict.getlist('filter')

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')

        match action:
            case 'toggle_interesting':
                self.toggle_interesting(request, *args, **kwargs)
            case 'toggle_liked':
                self.toggle_liked(request, *args, **kwargs)
            case _:
                pass
        return super().get(request, *args, **kwargs)

    def toggle_interesting(self, request, *args, **kwargs):
        feed_item_id = kwargs.get('id')
        user = request.user

        feed_item = self.model.objects.get(pk=feed_item_id)
        if hasattr(user, 'usersettings'):
            hidden_feed_items_qs = user.usersettings.hidden_feed_items
            if hidden_feed_items_qs.contains(feed_item):
                hidden_feed_items_qs.remove(feed_item)
            else:
                hidden_feed_items_qs.add(feed_item)
        else:
            usersettings = UserSettings(user=user)
            usersettings.save()
            usersettings.hidden_feed_items.add(feed_item)
        return feed_item

    def toggle_liked(self, request, *args, **kwargs):
        feed_item_id = kwargs.get('id')
        user = request.user

        feed_item = self.model.objects.get(pk=feed_item_id)
        if hasattr(user, 'usersettings'):
            liked_qs = user.usersettings.liked_feed_items
            if liked_qs.contains(feed_item):
                liked_qs.remove(feed_item)
            else:
                liked_qs.add(feed_item)
        else:
            usersettings = UserSettings(user=user)
            usersettings.save()
            usersettings.liked_feed_items.add(feed_item)
        return feed_item
