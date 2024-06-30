from django.contrib.auth.models import User
from django.forms import ModelForm
from django.views.generic import FormView



class ProfileEditForm(ModelForm):
    template_name_div = 'forms/div.html'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileEditView(FormView):
    form_class = ProfileEditForm
    template_name = 'profile/edit.html'
    success_url = '/profile/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    def form_valid(self, form):
        form.save()
        print('Form is valid')
        return super().form_valid(form)