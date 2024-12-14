
from feed.models import Collection
from feed.views.api.dialogs import NewCollectionView


class CollectionUpdateView(NewCollectionView):
    template_name = "dialogs/collection/update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = Collection.objects.get(pk=self.kwargs['collection_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('collection_id'):
            kwargs['instance'] = Collection.objects.get(pk=self.kwargs['collection_id'])
        return kwargs
