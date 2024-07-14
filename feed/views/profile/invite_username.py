from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView


class InviteUsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class InviteUsernameView(FormView):
    form_class = InviteUsernameForm
    template_name = 'profile/invite_username.html'

    def get_success_url(self):
        return reverse('invite_accept_password',
                       kwargs={'uidb64': self.kwargs['uidb64'], 'token': self.kwargs['token']})

    def get_form_kwargs(self):
        uid = urlsafe_base64_decode(self.kwargs['uidb64']).decode()
        user = User.objects.get(id=uid)
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: need to make a proper link validation
        context['validlink'] = True
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
