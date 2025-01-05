from django.contrib.auth import get_user_model
from django import forms
from django.forms import CharField
from django_registration.forms import RegistrationFormUniqueEmail, UserModel

class HiddenUsernameField(CharField):
    required = False
    disabled = True
    widget = forms.HiddenInput()

    def bound_data(self, data, initial):
        return initial

    def validate(self, value):
        pass

    def run_validators(self, value):
        pass

    def clean(self, value):
        return value

    def get_bound_field(self, form, field_name):
        bound_field = super().get_bound_field(form, field_name)
        return bound_field

    def _clean_bound_field(self, bf):
        return self.clean(bf.initial)


class RegistrationForm(RegistrationFormUniqueEmail):
    class Meta:
        fields = RegistrationFormUniqueEmail.Meta.fields
        model = get_user_model()
        field_classes = {UserModel.USERNAME_FIELD: HiddenUsernameField}