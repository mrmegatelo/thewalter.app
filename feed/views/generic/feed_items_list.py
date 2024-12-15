from django.utils.translation import gettext_noop as _
from django.views.generic import ListView

from feed.models import FeedItem, ServiceFeed
from feed.views.mixins import PageMetaMixin, FeedFiltersMixin


class GenericFeedItemListView(FeedFiltersMixin, PageMetaMixin, ListView):
    model = FeedItem
    paginate_by = 20
    title = _('My feed')

    def get_queryset(self):

        not_interesting = self.applied_filters.get('not_interesting', False)
        paid = self.applied_filters.get('paid', False)
        viewed = self.applied_filters.get('viewed', False)

        base_queryset = super().get_queryset()

        if not_interesting:
            not_interesting_qs = self.request.user.servicefeed_set.filter(type=ServiceFeed.Type.DISLIKED).first().feed_items.all()
            base_queryset = base_queryset.exclude(id__in=not_interesting_qs)

        if paid:
            paid_qs = self.model.objects.filter(has_paid_content=True)
            base_queryset = base_queryset.exclude(id__in=paid_qs)

        if viewed:
            viewed_qs = self.request.user.servicefeed_set.filter(type=ServiceFeed.Type.VIEWED).first().feed_items.all()
            base_queryset = base_queryset.exclude(id__in=viewed_qs)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']

        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        context['applied_filters_str'] = self.applied_filters_str

        return context

    @property
    def applied_filters_str(self):
        return '&'.join([f'filter={k}' for k, v in self.applied_filters.items() if v])
