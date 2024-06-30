from django.views.generic import TemplateView
from django.utils.translation import gettext_noop as _


class ProfileIndexView(TemplateView):
    template_name = 'profile/index.html'
    title = _('Profile')
