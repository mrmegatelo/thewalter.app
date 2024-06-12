from django.contrib.auth.mixins import LoginRequiredMixin


class ProtectedViewMixin(LoginRequiredMixin):
    login_url = '/login/'
