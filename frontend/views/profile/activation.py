from django_registration.backends.activation.views import ActivationView as BaseActivationView

from frontend.forms import ActivationForm


class ActivationView(BaseActivationView):
    form_class = ActivationForm