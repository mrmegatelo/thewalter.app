from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_registration.backends.activation.views import RegistrationView as BaseRegistrationView
from django.conf import settings


class RegistrationView(BaseRegistrationView):

    def send_activation_email(self, user):
        """
        Custom method to enable HTML activation emails.
        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context['user'] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        text_content = render_to_string(
            template_name='django_registration/activation_email_body.txt',
            context=context,
            request=self.request
        )
        html_content = render_to_string(
            template_name='django_registration/activation_email_body.html',
            context=context,
            request=self.request
        )

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content
        )