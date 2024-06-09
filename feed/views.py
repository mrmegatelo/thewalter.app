from django.views.generic import TemplateView, CreateView

from feed.forms import FeedForm


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Walter'
        context['new_feed_form'] = FeedForm()
        return context


class NewFeed(CreateView):
    form_class = FeedForm
    template_name = 'new_feed.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Feed'
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        # form.save()
        return super().form_valid(form)
