from django.views.generic import TemplateView


class ProfileIndexView(TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        return context
