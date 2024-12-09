from django.contrib.auth.views import LoginView


class ActivationSuccessView(LoginView):
    success_url = '/feed/'
    template_name = 'django_registration/activation_complete.html'