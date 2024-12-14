from django.urls import reverse
from django.views.generic import FormView

from feed.forms.collection import CollectionForm
from feed.views.mixins import PageMetaMixin, FeedContextMixin, FeedFiltersMixin


class CollectionCreate(FormView, PageMetaMixin, FeedContextMixin, FeedFiltersMixin):
    form_class = CollectionForm
    template_name = 'forms/collection/new.html'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "RefreshFeedList"
        return response

    def get_success_url(self):
        if self.request.headers.get('Hx-Request'):
            return reverse('api_dialog_hide')
        return reverse('new_collection')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_initial(self):
        return {"user": self.request.user}