from django.views.generic import FormView

from feed.forms import FeedForm
from feed.utils.helpers import normalize_url
from feed.views.api.dialogs.generic import GenericDialog


class NewFeed(FormView, GenericDialog):
    form_class = FeedForm
    template_name = 'dialogs/feed/new.html'
    dialog_position = "top"
    dialog_id = "new_feed"
    success_url = '/feed/new/success/?url={url}'

    def get_success_url(self):
        return self.success_url.format(url=self.get_form().data.get('url'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if kwargs.get('data'):
            url = kwargs.get('data').get('url')
        else:
            url = self.request.POST.get('url')
        if url is not None:
            url = normalize_url(url)

            kwargs['data'] = {'url': url}
        return kwargs
