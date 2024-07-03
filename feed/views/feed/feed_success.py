from django.views.generic import TemplateView

class Created(TemplateView):
    template_name = 'feed/success.html'
