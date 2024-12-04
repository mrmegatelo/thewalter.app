from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen, Request

import feedparser
from articulo import Articulo
from django.db.models import Q
from django.http import QueryDict

from feed.models import Attachment
from feed.utils.enums import FeedContentTypes


def get_url_content_type(url):
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
        },
    )
    res = urlopen(req)
    http_message = res.info()
    return http_message.get_content_type()


def get_wrapped_url(url):
    wrapped_url = urlparse("http://splash:8050/render.html")
    params = QueryDict(mutable=True)
    params.update({"url": url})
    params.update({"engine": "chromium"})
    params.update({"wait": 1})
    wrapped_url = wrapped_url._replace(query=params.urlencode())
    return urlunparse(wrapped_url)


def normalize_url(url, base_path=None):
    """
    URL normalization helper function.
    - Adds / as a path if no path is given.
    :param base_path:
    :param url:
    :return:
    """
    parsed_url = urlparse(url)

    if parsed_url.scheme == "":
        parsed_url = parsed_url._replace(scheme="https")
    if parsed_url.path == "":
        parsed_url = parsed_url._replace(path="/")
    if parsed_url.netloc == "" and base_path is not None:
        base_path = urlparse(base_path)
        parsed_url = base_path._replace(path=parsed_url.path)

    return str(urlunparse(parsed_url))


def filter_by_feed_type(queryset, feed_type):
    """
    Filter queryset by feed type.
    :param queryset: 
    :param feed_type: 
    :return: 
    """
    match feed_type:
        case "podcasts":
            return queryset.filter(attachments__type=Attachment.Type.AUDIO)
        case "videos":
            return queryset.filter(
                Q(attachments__type=Attachment.Type.VIDEO)
                | Q(attachments__type=Attachment.Type.EMBED)
            )
        case "articles":
            return queryset.filter(attachments__isnull=True)
        case _:
            return queryset


def get_articulo_instance(url_or_content, content_type=None):
    if content_type is None:
        content_type = get_url_content_type(url_or_content)
    if content_type == FeedContentTypes.TEXT_HTML.value:
        return Articulo(url_or_content)
    parsed = feedparser.parse(url_or_content)
    return Articulo(parsed.feed.get("link") or parsed.feed.get("href"))
