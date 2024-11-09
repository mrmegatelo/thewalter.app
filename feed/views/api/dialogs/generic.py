from django.views.generic.base import ContextMixin


class GenericDialog(ContextMixin):
    dialog_position = "top"
    dialog_id = None
    dialog_id_key = "dialog_id"
    dialog_position_key = "dialog_position"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data[self.dialog_id_key] = self.dialog_id
        context_data[self.dialog_position_key] = self.dialog_position
        return context_data
