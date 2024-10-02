from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen, Request

import feedparser
from articulo import Articulo
from django.db.models import Q

from feed.models import Attachment
from feed.utils.enums import FeedContentTypes
from feed.utils.feed_parsers import HTMLFeedParser, RSSFeedParser
from feed.utils.feed_validators import RSSLinkValidator, HTMLLinkValidator


def get_url_content_type(url):
    req = Request(url, headers={
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"})
    res = urlopen(req)
    http_message = res.info()
    return http_message.get_content_type()


def normalize_url(url):
    """
    URL normalization helper function.
    - Adds / as a path if no path is given.
    :param url:
    :return:
    """
    parsed_url = urlparse(url)
    if parsed_url.path == '':
        parsed_url = parsed_url._replace(path='/')
    return urlunparse(parsed_url)


def filter_by_attachments_type(queryset, attachments_type):
    match attachments_type:
        case 'podcasts':
            return queryset.filter(attachments__type=Attachment.Type.AUDIO)
        case 'videos':
            return queryset.filter(
                Q(attachments__type=Attachment.Type.VIDEO) | Q(attachments__type=Attachment.Type.EMBED))
        case 'articles':
            return queryset.filter(attachments__isnull=True)
        case _:
            return queryset


def get_form_parser(url, articulo):
    content_type = get_url_content_type(url)
    if content_type == FeedContentTypes.TEXT_HTML.value:
        return HTMLFeedParser(articulo)
    return RSSFeedParser(articulo)


def get_form_validator(url, articulo):
    content_type = get_url_content_type(url)
    match content_type:
        case FeedContentTypes.TEXT_HTML.value:
            return HTMLLinkValidator(articulo)
        case FeedContentTypes.TEXT_XML.value \
             | FeedContentTypes.APPLICATION_XML.value \
             | FeedContentTypes.APPLICATION_XML_RSS.value \
             | FeedContentTypes.APPLICATION_XML_ATOM.value:
            return RSSLinkValidator(articulo)


def get_articulo_instance(url):
    content_type = get_url_content_type(url)
    if content_type == FeedContentTypes.TEXT_HTML.value:
        return Articulo(url)
    parsed = feedparser.parse(url)
    return Articulo(parsed.feed.get('link') or parsed.feed.get('href'))
