from datetime import datetime

from django.views.generic import TemplateView

from feed.models import WaitlistRequest
from feed.views.mixins import PageMetaMixin


class Index(TemplateView, PageMetaMixin):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        real_subscriptions = WaitlistRequest.objects.count()
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        context['subscribers_count'] = real_subscriptions + now.day + now.hour + now.minute
        return context
