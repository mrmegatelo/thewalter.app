from django.views.generic import TemplateView
from django.utils.translation import gettext_noop as _

from feed.views.mixins import PageMetaMixin


class Created(TemplateView, PageMetaMixin):
    template_name = 'feed/success.html'
    title = _('My feed')
