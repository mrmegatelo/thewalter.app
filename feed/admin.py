from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Feed, FeedItem, UserSettings, WaitlistRequest


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False
    verbose_name_plural = 'User Settings'


class UserAdmin(BaseUserAdmin):
    inlines = [UserSettingsInline]


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'pub_date']
    prepopulated_fields = {'slug': ('title',)}


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'pub_date']
    list_filter = ['feed']
    search_fields = ['title', 'description']


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(WaitlistRequest)
