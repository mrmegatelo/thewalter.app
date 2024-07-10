from django.views.generic import CreateView
from django.utils.translation import gettext_noop as _

from feed.forms import FeedForm
from feed.models import Feed
from feed.views.mixins import PageMetaMixin


class Create(CreateView, PageMetaMixin):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed/new/success/'
    title = _('New Feed')

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object.subscribers.add(self.request.user)
        return result

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        url = self.request.POST.get('url')
        if url is not None:
            try:
                existing_feed = Feed.objects.get(url=url)
            except Feed.DoesNotExist:
                existing_feed = Feed.objects.create(url=url)

            kwargs['instance'] = existing_feed

        return kwargs
