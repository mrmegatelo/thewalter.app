from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Register your models here.
from .models import (
    Feed,
    FeedItem,
    UserSettings,
    WaitlistRequest,
    Invite,
    Attachment,
    ServiceFeed,
)
from .tasks import parse_feed


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False
    verbose_name_plural = 'User Settings'


class AttachmentInline(admin.TabularInline):
    model = Attachment
    can_delete = True
    verbose_name_plural = 'Attachments'


class UserAdmin(BaseUserAdmin):
    inlines = [UserSettingsInline]


@admin.action(description='Restart parsing')
def restart_parsing_task(_model, _request, queryset):
    for feed in queryset:
        parse_feed.delay(feed.id, True)


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'pub_date']
    prepopulated_fields = {'slug': ('title',)}
    actions = [restart_parsing_task]


class ServiceFeedAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']
    list_filter = ['type', 'user']


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'pub_date']
    list_filter = ['feed', 'service_feeds']
    search_fields = ['title', 'description']
    inlines = [AttachmentInline]


@admin.action(description='Send selected invites')
def send_invite(_model, request, queryset):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    for invite in queryset:
        user = invite.user
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        context = {
            'domain': domain,
            'site_name': site_name,
            "protocol": "https",
            'uid': uid,
            'token': token
        }
        from_email = 'no-reply@thewalter.app'
        to_email = invite.user.email

        subject = loader.render_to_string('emails/registration/invite_subject.txt', context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string('emails/registration/invite_text.html', context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        html_email = loader.render_to_string('emails/registration/invite.html', context)
        email_message.attach_alternative(html_email, "text/html")

        email_message.send()

        invite.status = Invite.Status.SENT
        invite.sent_at = timezone.now()
        invite.save()


class InviteAdmin(admin.ModelAdmin):
    list_display = ['status', 'user', 'created_at', 'sent_at', 'accepted_at', 'activated_at']
    list_editable = ['user']
    list_filter = ['status']
    search_fields = ['email']
    actions = [send_invite]


class WaitlistRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'invite']
    list_filter = ['invite__status']
    list_editable = ['invite']


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(ServiceFeed, ServiceFeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(WaitlistRequest, WaitlistRequestAdmin)
