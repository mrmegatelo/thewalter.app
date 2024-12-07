from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, CreateView

from feed.forms.registration import RegistrationForm


class WaitlistView(CreateView):
    form_class = RegistrationForm
    model = get_user_model()
    template_name = "registration/index.html"
    success_url = "success"


class WaitlistSuccessView(TemplateView):
    template_name = "waitlist/success.html"
