from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import EmailField
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    email = EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email']