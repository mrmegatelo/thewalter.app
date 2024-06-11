from django.apps import AppConfig
from django.db.models.signals import post_save


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    def ready(self):
        from feed.models import Feed
        from feed.tasks import parse_feed

        def my_handler(sender, instance, **kwargs):
            parse_feed.delay(instance.pk)
        post_save.connect(my_handler, sender=Feed)
