from datetime import datetime

from django.views.generic import TemplateView
from django.conf import settings

from feed.models import WaitlistRequest


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        print(self.request.META.get("REMOTE_ADDR"), settings.INTERNAL_IPS, settings.DEBUG)
        real_subscriptions = WaitlistRequest.objects.count()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        context['description'] = 'The only feed you need.'
        context['cover_img'] = 'feed/img/cover.jpg'
        now = datetime.now()
        context['subscribers_count'] = real_subscriptions + now.day + now.hour + now.minute
        return context
