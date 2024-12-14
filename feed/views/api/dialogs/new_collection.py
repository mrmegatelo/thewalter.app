from django.views.generic import FormView

from feed.forms import CollectionForm
from feed.views.api.dialogs.generic import GenericDialog


class NewCollectionView(FormView, GenericDialog):
    form_class = CollectionForm
    template_name = "dialogs/collection/new.html"
    dialog_position = "top"
    dialog_id = "new_collection"
    success_url = "/dialogs/hide"

    def get_initial(self):
        return {"user": self.request.user}
