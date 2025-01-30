from django.views.generic.base import ContextMixin
from django.utils.translation import gettext_noop as _



class PageMetaMixin(ContextMixin):
    title = "thewalter.app"
    description = _("The only feed you need.")
    cover = "img/cover.jpg"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title,
                "description": self.description,
                "cover": self.cover,
            }
        )
        return context
