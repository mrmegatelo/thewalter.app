from django.views.generic import TemplateView

from feed.views.api.dialogs.generic import GenericDialog


class DialogHide(GenericDialog, TemplateView):
    template_name = 'dialogs/hide.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "RefreshFeedList"
        return response