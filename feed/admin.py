from django.contrib import admin

# Register your models here.
from .models import Feed, FeedItem


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'pub_date']
    prepopulated_fields = {'slug': ('title',)}


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'pub_date']
    list_filter = ['feed']
    search_fields = ['title', 'description']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
