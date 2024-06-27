from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        context['description'] = 'The only feed you need.'
        context['cover_img'] = '/static/feed/img/cover.jpg'
        return context
