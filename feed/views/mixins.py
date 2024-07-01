from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.utils.translation import gettext_noop as _


class ProtectedViewMixin(LoginRequiredMixin):
    login_url = '/profile/login/'


class PageMetaMixin(ContextMixin):
    title = 'thewalter.app'
    description = _('The only feed you need.')
    cover = 'feed/img/cover.jpg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'description': self.description,
            'cover': self.cover,
        })
        return context
