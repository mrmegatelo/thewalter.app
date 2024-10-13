from django.db.models import Q
from django.views.generic import FormView
from django.utils.translation import gettext_noop as _
from django.views.generic.edit import ModelFormMixin

from feed.forms import FeedForm
from feed.models import Feed
from feed.utils.helpers import normalize_url, get_form_parser, get_articulo_instance, get_form_validator
from feed.views.mixins import PageMetaMixin, FeedContextMixin, FeedFiltersMixin


class FeedCreate(ModelFormMixin, FormView, PageMetaMixin, FeedContextMixin, FeedFiltersMixin):
    form_class = FeedForm
    template_name = 'feed/new.html'
    success_url = '/feed/new/success/?url={url}'
    title = _('My feed')
    object = None

    def form_valid(self, form):
        result = super().form_valid(form)
        # self.object.subscribers.add(self.request.user)
        # return self.render_to_response(self.get_context_data(form=form))
        return result

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if kwargs.get('data'):
            url = kwargs.get('data').get('url')
        else:
            url = self.request.POST.get('url')
        if url is not None:
            url = normalize_url(url)
            articulo = get_articulo_instance(url)
            try:
                self.object = Feed.objects.get(Q(url=url) | Q(rss_url=url))
            except Feed.DoesNotExist:
                print('no feed found')

            kwargs['data'] = {'url': url}
            kwargs['feed_parser'] = get_form_parser(url, articulo)
            kwargs['validator'] = get_form_validator(url, articulo)
        return kwargs
