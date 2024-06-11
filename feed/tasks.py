from celery import shared_task
from feed.models import Feed


@shared_task()
def parse_feed(pk):
    feed = Feed.objects.get(pk=pk)
    print(feed.rss_url, 'test')
    print("Parsing feed", vars(feed))
    return pk
