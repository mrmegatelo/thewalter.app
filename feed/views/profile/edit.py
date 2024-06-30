from django.contrib.auth.models import User
from django.forms import ModelForm
from django.views.generic import FormView
from django.utils.translation import gettext_noop as _

from feed.views.mixins import PageMetaMixin


class ProfileEditForm(ModelForm):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileEditView(FormView, PageMetaMixin):
    form_class = ProfileEditForm
    template_name = 'profile/edit.html'
    success_url = '/profile/'
    title = _('Edit Profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
