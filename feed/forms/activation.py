from django import forms
from django_registration.backends.activation.forms import ActivationForm as BaseActivationForm


class ActivationForm(BaseActivationForm):
    activation_key = forms.CharField(widget=forms.HiddenInput)

    def clean_activation_key(self):
        return super().clean_activation_key()

