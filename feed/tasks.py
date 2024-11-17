import time

import requests
from celery import shared_task
import feedparser
from articulo import Articulo
from django.db.models import Q
from requests import HTTPError

from feed.models import Feed, FeedItem, Attachment
from feed.utils.enums import (
    AudioMimeTypes,
    VideoMimeTypes,
    FeedMediaContentMediums,
    FeedContentTypes,
)
from feed.utils.helpers import get_wrapped_url, normalize_url
from feed.utils.feed_parsers import get_form_parser, RSSFeedParser

AUDIO_MIME_TYPES_SET = set([t.value for t in AudioMimeTypes])


def parse_attachments(entry, feed):
    """
    Parses feed item attachments.
    :param entry:
    :param feed:
    :return:
    """
    if entry.get("yt_videoid"):
        return parse_yt_video(entry, feed)
    enclosure_types_set = set([e.get("type") for e in entry.get("enclosures", [])])

    if len(enclosure_types_set) > 0 and enclosure_types_set.issubset(
        AUDIO_MIME_TYPES_SET
    ):
        return parse_audio_enclosures(entry, feed)

    if FeedMediaContentMediums.VIDEO.value in [
        m.get("medium") for m in entry.get("media_content", [])
    ]:
        return parse_media(entry, feed)


def parse_yt_video(entry, feed_item):
    """
    Parses feed item as a YouTube video.
    :param entry:
    :param feed_item:
    :return:
    """
    video_id = entry.get("yt_videoid")
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return Attachment.objects.create(
        url=embed_url, type=Attachment.Type.EMBED, feed_item=feed_item
    )


def parse_feed_item(entry, feed) -> tuple[FeedItem, bool]:
    """
    Parses a feed item.
    :param entry:
    :param feed:
    :return:
    """
    article_content,_ = get_feed_content_by_url(entry.link)
    article = Articulo(article_content)
    normalized_preview = None
    parsed_pud_date = entry.get("published_parsed") or entry.get("updated_parsed")

    if article.preview and article.preview != b'':
        normalized_preview = normalize_url(article.preview)
    return FeedItem.objects.update_or_create(
        link=entry.link,
        defaults={
            "feed": feed,
            "title": entry.title,
            "description": entry.get("summary", ""),
            "pub_date": time.strftime("%Y-%m-%dT%H:%M:%SZ", parsed_pud_date),
            "preview": normalized_preview,
            "has_paid_content": article.has_paywall,
        }
    )


def parse_audio_enclosures(entry, feed_item):
    """
    Parses "enclosure" part of feed item.
    :param entry:
    :param feed_item:
    :return:
    """
    for enclosure in entry.get("enclosures"):
        if enclosure.get("type") in AUDIO_MIME_TYPES_SET:
            Attachment.objects.create(
                url=enclosure.href, type=Attachment.Type.AUDIO, feed_item=feed_item
            )


def parse_media(entry, feed_item):
    """
    Parses "media" part of feed item.
    :param entry:
    :param feed_item:
    :return:
    """
    for media_item in entry.get("media_content"):
        if media_item.get("medium") != FeedMediaContentMediums.VIDEO.value:
            continue

        if media_item.get("type") == VideoMimeTypes.VIDEO_MP4.value:
            return Attachment.objects.create(
                url=media_item.get("url"),
                type=Attachment.Type.VIDEO,
                feed_item=feed_item,
            )

        else:
            return Attachment.objects.create(
                url=entry.get("media_player").get("url"),
                type=Attachment.Type.EMBED,
                feed_item=feed_item,
            )


@shared_task()
def parse_feed(pk, force = False):
    """
    Parse the feed and save the items to the database
    :param force:
    :param pk:
    :return:
    """
    feed = Feed.objects.get(pk=pk)
    try:
        feed_content,_ = get_feed_content_by_url(feed.rss_url)
        article = Articulo(feed.url)
        parser = RSSFeedParser(article)
        for feed_meta in parser.parse(feed_content):
            if force:
                feed.icon = feed_meta.icon_url
                feed.description = feed_meta.description
                feed.title = feed_meta.title
                feed.save()
            for entry in feed_meta.entries:
                if not FeedItem.objects.filter(link=entry.link).exists() or force:
                    feed_item, created = parse_feed_item(entry, feed)
                    # TODO: need to improve attachment parsing logic for the update case
                    if created:
                        parse_attachments(entry, feed_item)
    except Exception as e:
        print(f"Problem parsing feed: {e}")


@shared_task()
def update_feeds():
    """
    Update all feeds
    :return:
    """
    for feed in Feed.objects.all():
        parse_feed.delay(feed.pk)


def get_feed_by_url(url):
    return Feed.objects.filter(Q(url__contains=url) | Q(rss_url__contains=url)).all().values()


def get_url_content(url, on_error=None, **kwargs):
    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        content_type = [
            s.strip() for s in response.headers.get("content-type").split(";")
        ][0]

        return response.text, content_type
    except HTTPError as e:
        if on_error is None:
            raise e

        status_code = e.response.status_code
        match status_code:
            case 403 | 406:
                return on_error(url, **kwargs)
            case _:
                raise e


def get_url_content_with_fake_browser(url, **kwargs):
    url = get_wrapped_url(url)
    return get_url_content(url)


def get_url_content_with_headers(url, **kwargs):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3",
        "Accept": "text/html, text/xml, application/xml, application/rss+xml, application/atom+xml",
    }

    return get_url_content(url, headers=headers, on_error=get_url_content_with_proxy, **kwargs)


def get_url_content_with_proxy(url, **kwargs):
    proxies = {
        "http": "socks5://proxy:9150",
        "https": "socks5://proxy:9150",
    }
    return get_url_content(
        url, proxies=proxies, on_error=get_url_content_with_fake_browser, **kwargs
    )


def get_feed_content_by_url(url):
    return get_url_content(url, on_error=get_url_content_with_headers)


def get_articulo_instance(url_or_content, content_type):
    if content_type == FeedContentTypes.TEXT_HTML.value:
        return Articulo(url_or_content)
    parsed = feedparser.parse(url_or_content)
    url_or_content = parsed.feed.get('link') or parsed.feed.get('href')
    rss_content,_ = get_feed_content_by_url(url_or_content)
    return Articulo(rss_content)


def parse_feeds_by_url(url):
    try:
        feed_content, content_type = get_feed_content_by_url(url)
        articulo = get_articulo_instance(feed_content, content_type)
        parser = get_form_parser(content_type, articulo)

        feeds = []

        for link_meta in parser.parse(url):
            feed = Feed(
                title=link_meta.title,
                url=link_meta.url,
                description=link_meta.description,
                rss_url=link_meta.rss_url,
                icon=link_meta.icon_url,
            )
            feed.save()
            feeds.append(feed.id)
        return feeds
    except HTTPError:
        return []


@shared_task()
def parse_feed_info(url):
    result = []
    feed_list = get_feed_by_url(url)
    if len(feed_list) == 0:
        return parse_feeds_by_url(url)

    for feed in feed_list:
        result.append(feed["id"])
    return result
