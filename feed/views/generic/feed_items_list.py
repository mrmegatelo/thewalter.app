from django.db.models import Q
from django.utils.translation import gettext_noop as _
from django.views.generic import ListView

from feed.models import FeedItem, FeedItemAction
from feed.views.mixins import PageMetaMixin, FeedFiltersMixin


class GenericFeedItemListView(FeedFiltersMixin, PageMetaMixin, ListView):
    model = FeedItem
    paginate_by = 20
    title = _("My feed")

    def get_queryset(self):
        base_queryset = super().get_queryset()
        base_queryset = self.__get_queryset_with_filters(base_queryset)
        base_queryset = self.__get_queryset_with_search(base_queryset)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context["page_obj"]

        context["paginator_range"] = page.paginator.get_elided_page_range(
            page.number, on_each_side=2, on_ends=1
        )
        context["applied_filters_str"] = self.applied_filters_str

        return context

    @property
    def applied_filters_str(self):
        return "&".join([f"filter={k}" for k, v in self.applied_filters.items() if v])

    def __get_queryset_with_search(self, queryset):
        search_term = self.request.GET.get("search")
        if search_term:
            return queryset.filter(
                Q(title__icontains=search_term) | Q(description__icontains=search_term)
            )
        return queryset

    def __get_queryset_with_filters(self, queryset):
        not_interesting = self.applied_filters.get("not_interesting", False)
        paid = self.applied_filters.get("paid", False)
        viewed = self.applied_filters.get("viewed", False)

        temp_viewed = self.request.session.get(f"viewed_{self.request.path}", [])

        if not_interesting:
            not_interesting_qs = self.request.user.feeditemaction_set.filter(
                type=FeedItemAction.Type.DISLIKE
            )
            queryset = queryset.exclude(actions__in=not_interesting_qs)

        if paid:
            paid_qs = self.model.objects.filter(has_paid_content=True)
            queryset = queryset.exclude(id__in=paid_qs)

        if viewed:
            viewed_qs = self.request.user.feeditemaction_set.filter(
                type=FeedItemAction.Type.VIEW
            )
            queryset = queryset.exclude(actions__in=viewed_qs).exclude(
                actions__in=temp_viewed
            )
        return queryset
