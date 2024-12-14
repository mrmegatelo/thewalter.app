from django.views.generic import TemplateView

from feed.views.api.dialogs.generic import GenericDialog


class DialogHide(GenericDialog, TemplateView):
    template_name = 'dialogs/hide.html'
    pass