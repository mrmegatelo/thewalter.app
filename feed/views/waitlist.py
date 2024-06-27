from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse

from feed.models import WaitlistRequest


class WaitlistView(TemplateView):
    def post(self, request):
        email = request.POST.get('email')

        if not email:
            return render(request, 'forms/waitlist.html', {'error': 'Email is required.'})

        # Corner cases:
        # 1. User is already registered.
        users_qs = User.objects.filter(email=email)
        if users_qs.exists():
            return render(request, 'forms/waitlist.html',
                          {'error': 'User is already registered.', 'email': email}
                          )

        # 2. User is already in the waitlist.
        waitlist_qs = WaitlistRequest.objects.filter(email=email)
        if waitlist_qs.exists():
            return render(request, 'forms/waitlist.html', {
                'error': 'User is already on the waitlist.', 'email': email
            })

        WaitlistRequest.objects.create(email=email)
        response = render(request, 'forms/waitlist.html')
        success_url = 'waitlist_success'
        response.headers['HX-Redirect'] = reverse(success_url)
        return response


class WaitlistSuccessView(TemplateView):
    template_name = 'waitlist/success.html'
