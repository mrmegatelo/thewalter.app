from urllib.parse import urlparse, urlunparse

from django.core.paginator import InvalidPage
from django.http import QueryDict, Http404
from django.urls import resolve
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin

from feed.models import Feed
from feed.utils.helpers import filter_by_attachments_type
from feed.views.generic.feed_items_list import FeedFiltersMixin, GenericFeedItemListView


class FullFeedList(GenericFeedItemListView):
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
            return paginator, page, page.object_list, page.has_other_pages()
        except InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )


class UserFeedList(FullFeedList):
    http_method_names = ['get']

    def get_queryset(self):
        feed_type = self.request.GET.get('feed_type')
        queryset = super().get_queryset()

        if feed_type:
            queryset = filter_by_attachments_type(queryset, feed_type)
        return queryset.filter(feed__subscribers=self.request.user)


class FeedItemListView(FullFeedList):
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super().get_queryset()
        feed_id = self.kwargs.get('feed_id')
        return queryset.filter(feed__id=feed_id)


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
        return response


class FeedTypes(TemplateView, ContextMixin):
    http_method_names = ['post']
    template_name = 'blocks/feed/types_selector.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_type'] = self.request.POST.get('feed_type')
        return context

    def post(self, request, *args, **kwargs):
        url = urlparse(request.headers.get('Referer'))
        query_dict = QueryDict(url.query, mutable=True)
        feed_type = self.request.POST.getlist('feed_type')
        if 'none' not in feed_type:
            query_dict.setlist('feed_type', feed_type)
        else:
            query_dict.pop('feed_type')

        url = url._replace(query=query_dict.urlencode())
        url = urlunparse(url)
        response = super().get(request, *args, **kwargs)
        response.headers['HX-Redirect'] = url
        return response


class FeedItemActions(FullFeedList):
    http_method_names = ['post']

    def get_queryset(self):
        queryset = super().get_queryset()
        parsed_url = urlparse(self.request.headers.get('hx-current-url'))
        match = resolve(parsed_url.path)
        query = QueryDict(parsed_url.query, mutable=False)
        feed_slug = match.kwargs.get('slug')
        feed_type = query.get('feed_type')

        if feed_slug:
            return queryset.filter(feed__slug=feed_slug)
        if feed_type:
            return filter_by_attachments_type(queryset, feed_type)
        return queryset

    def init_filters(self, request):
        url = urlparse(request.headers.get('hx-current-url'))
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
        feed_item_id = kwargs.get('feed_item_id')
        user = request.user

        feed_item = self.model.objects.get(pk=feed_item_id)
        disliked_qs = user.servicefeed_set.filter(type='disliked').first().feed_items
        if disliked_qs.contains(feed_item):
            disliked_qs.remove(feed_item)
        else:
            disliked_qs.add(feed_item)
        return feed_item

    def toggle_liked(self, request, *args, **kwargs):
        feed_item_id = kwargs.get('feed_item_id')
        user = request.user

        feed_item = self.model.objects.get(pk=feed_item_id)
        liked_qs = user.servicefeed_set.filter(type='liked').first().feed_items

        if liked_qs.contains(feed_item):
            liked_qs.remove(feed_item)
        else:
            liked_qs.add(feed_item)

        return feed_item


class FeedUnsubscribe(DetailView):
    http_method_names = ['post']
    template_name = 'blocks/feed/subscription.html'
    model = Feed
    pk_url_kwarg = 'feed_id'

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        match action:
            case 'unsubscribe':
                self.unsubscribe(request, *args, **kwargs)
            case 'subscribe':
                self.subscribe(request, *args, **kwargs)

        response = super().get(request, *args, **kwargs)
        response.headers['HX-Trigger'] = 'refresh_feed'
        return response

    def subscribe(self, request, *args, **kwargs):
        feed_id = kwargs.get('feed_id')
        feed = Feed.objects.get(pk=feed_id)
        feed.subscribers.add(request.user)
        feed.save()

    def unsubscribe(self, request, *args, **kwargs):
        feed_id = kwargs.get('feed_id')
        feed = Feed.objects.get(pk=feed_id)
        feed.subscribers.remove(request.user)
        feed.save()
