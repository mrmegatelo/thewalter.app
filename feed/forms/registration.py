from django.forms import ModelForm, EmailField
from django.contrib.auth import get_user_model

class RegistrationForm(ModelForm):
    email = EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['email']