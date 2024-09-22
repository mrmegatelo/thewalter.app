from django.apps import AppConfig
from django.db.models.signals import post_save


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    def ready(self):
        from feed.models import Feed, ServiceFeed, UserSettings
        from feed.tasks import parse_feed
        from django.contrib.auth.models import User

        def feed_parse_handler(sender, instance, **kwargs):
            parse_feed.delay(instance.pk)

        def usersettings_handler(sender, instance: User, **kwargs):
            try:
                instance.usersettings
            except UserSettings.DoesNotExist:
                instance.usersettings = UserSettings.objects.create(user=instance)
                instance.usersettings.save()

            for service_feed_type in ['liked', 'disliked', 'podcasts', 'articles', 'videos']:
                if not instance.servicefeed_set.filter(type=service_feed_type).exists():
                    service_feed = ServiceFeed.objects.create(user=instance, type=service_feed_type)
                    instance.servicefeed_set.add(service_feed)

        post_save.connect(feed_parse_handler, sender=Feed, weak=False)
        post_save.connect(usersettings_handler, sender=User, weak=False)
