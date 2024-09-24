import time

from celery import shared_task
import feedparser
from articulo import Articulo
from feed.models import Feed, FeedItem, Attachment


@shared_task()
def parse_feed(pk):
    """
    Parse the feed and save the items to the database
    :param pk:
    :return:
    """
    feed = Feed.objects.get(pk=pk)
    try:
        feed_data = feedparser.parse(feed.rss_url)
        for entry in feed_data.entries:
            if not FeedItem.objects.filter(link=entry.link).exists():
                article = Articulo(entry.link)
                parsed_pud_date =  entry.get('published_parsed') or entry.get('updated_parsed')

                feed_item = FeedItem.objects.create(
                    title=entry.title,
                    description=entry.summary,
                    link=entry.link,
                    pub_date=time.strftime('%Y-%m-%dT%H:%M:%SZ', parsed_pud_date),
                    feed=feed,
                    has_paid_content=article.has_paywall
                )

                for enclosure in entry.enclosures:
                    if enclosure.type == 'audio/mpeg' or enclosure.type == 'audio/mp3':
                        Attachment.objects.create(
                            url=enclosure.href,
                            type=Attachment.Type.AUDIO,
                            feed_item=feed_item
                        )
    except Exception as e:
        print(e)


@shared_task()
def update_feeds():
    """
    Update all feeds
    :return:
    """
    for feed in Feed.objects.all():
        parse_feed.delay(feed.pk)
