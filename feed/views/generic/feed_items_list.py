from django.utils.translation import gettext_noop as _
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import ContextMixin

from feed.models import FeedItem
from feed.views.mixins import PageMetaMixin


class FeedFiltersMixin(ContextMixin, View):
    applied_filters = {'not_interesting': True}

    def setup(self, request, *args, **kwargs):
        filters = self.init_filters(request)
        if filters:
            new_filters = dict()
            for name in filters:
                new_filters[name] = True
            self.applied_filters = new_filters
        return super().setup(request, *args, **kwargs)

    def init_filters(self, request):
        request_params = request.GET if request.method == 'GET' else request.POST
        return request_params.getlist('filter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applied_filters'] = self.applied_filters
        return context


class GenericFeedItemListView(FeedFiltersMixin, PageMetaMixin, ListView):
    model = FeedItem
    paginate_by = 20
    title = _('My feed')

    def get_queryset(self):

        not_interesting = self.applied_filters.get('not_interesting', False)
        paid = self.applied_filters.get('paid', False)

        base_queryset = super().get_queryset()

        if not_interesting:
            not_interesting_qs = self.request.user.servicefeed_set.filter(type='disliked').first().feed_items.all()
            base_queryset = base_queryset.exclude(id__in=not_interesting_qs)

        if paid:
            paid_qs = self.model.objects.filter(has_paid_content=True)
            base_queryset = base_queryset.exclude(id__in=paid_qs)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']

        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        context['applied_filters_str'] = self.applied_filters_str
        context['liked'] = self.request.user.servicefeed_set.filter(type='liked').first()
        context['disliked'] = self.request.user.servicefeed_set.filter(type='disliked').first()

        return context

    @property
    def applied_filters_str(self):
        return '&'.join([f'filter={k}' for k, v in self.applied_filters.items() if v])
