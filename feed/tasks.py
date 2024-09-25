import time

from celery import shared_task
import feedparser
from articulo import Articulo
from feed.models import Feed, FeedItem, Attachment

AUDIO_MIME_TYPES_SET = {'audio/mpeg', 'audio/mp3', 'audio/x-m4a'}


def parse_attachments(entry, feed):
    if entry.get('yt_videoid'):
        return parse_yt_video(entry, feed)
    enclosure_types_set = set([e.get('type') for e in entry.get('enclosures', [])])

    if len(enclosure_types_set) > 0 and enclosure_types_set.issubset(AUDIO_MIME_TYPES_SET):
        return parse_audio_enclosures(entry, feed)

    if 'video' in [m.get('medium') for m in entry.get('media_content', [])]:
        return parse_media(entry, feed)


def parse_yt_video(entry, feed_item):
    video_id = entry.get('yt_videoid')
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return Attachment.objects.create(
        url=embed_url,
        type=Attachment.Type.EMBED,
        feed_item=feed_item
    )


def parse_feed_item(entry, feed) -> FeedItem:
    article = Articulo(entry.link)
    parsed_pud_date = entry.get('published_parsed') or entry.get('updated_parsed')

    return FeedItem.objects.create(
        title=entry.title,
        description=entry.get('summary', ""),
        link=entry.link,
        pub_date=time.strftime('%Y-%m-%dT%H:%M:%SZ', parsed_pud_date),
        feed=feed,
        has_paid_content=article.has_paywall
    )


def parse_audio_enclosures(entry, feed_item):
    for enclosure in entry.get('enclosures'):
        if enclosure.get('type') in AUDIO_MIME_TYPES_SET:
            Attachment.objects.create(
                url=enclosure.href,
                type=Attachment.Type.AUDIO,
                feed_item=feed_item
            )


def parse_media(entry, feed_item):
    for media_item in entry.get('media_content'):
        if media_item.get('medium') != 'video':
            continue

        if media_item.get('type') == 'video/mp4':
            return Attachment.objects.create(
                url=media_item.get('url'),
                type=Attachment.Type.VIDEO,
                feed_item=feed_item
            )

        else:
            return Attachment.objects.create(
                url=entry.get('media_player').get('url'),
                type=Attachment.Type.EMBED,
                feed_item=feed_item
            )


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
                feed_item = parse_feed_item(entry, feed)
                parse_attachments(entry, feed_item)
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
