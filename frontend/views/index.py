from django.shortcuts import redirect
from django.views.generic import TemplateView

from frontend.views.mixins import PageMetaMixin


class Index(TemplateView, PageMetaMixin):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/feed/")
        return super().get(request, *args, **kwargs)
