from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    def ready(self):
        from feed.models import Feed, UserSettings
        from feed.tasks import parse_feed
        from django.contrib.auth.models import User

        def feed_parse_hadler(sender, instance, **kwargs):
            parse_feed.delay(instance.pk)

        def usersettings_hadler(sender, instance, **kwargs):
            try:
                instance.usersettings
            except UserSettings.DoesNotExist:
                instance.usersettings = UserSettings.objects.create(user=instance)
                instance.usersettings.save()

        post_save.connect(feed_parse_hadler, sender=Feed)
        pre_save.connect(usersettings_hadler, sender=User)
