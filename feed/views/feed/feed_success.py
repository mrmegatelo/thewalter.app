from django.views.generic import TemplateView

from feed.views.mixins import ProtectedViewMixin


class Created(ProtectedViewMixin, TemplateView):
    template_name = 'feed/success.html'
