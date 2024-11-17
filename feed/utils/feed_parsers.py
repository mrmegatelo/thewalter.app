from collections.abc import Generator
from urllib.parse import urlparse, urlunparse
from abc import ABC, abstractmethod
from dataclasses import dataclass

import feedparser
from articulo import Articulo
from feedparser import FeedParserDict

from feed.utils.enums import FeedContentTypes
from feed.utils.helpers import normalize_url


@dataclass
class FeedMeta:
    title: str
    description: str
    icon_url: str
    rss_url: str
    url: str
    entries: list

class AbstractFeedParser(ABC):

    articulo: Articulo

    def __init__(self, articulo: Articulo):
        self.articulo = articulo

    @abstractmethod
    def parse(self, url: str) -> FeedMeta:
        pass


class RSSFeedParser(AbstractFeedParser):
    def parse(self, url: str) -> Generator[FeedMeta]:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3",
            "Accept": "text/html, text/xml, application/xml, application/rss+xml, application/atom+xml",
        }
        parsed = feedparser.parse(url, request_headers=headers)
        parsed_icon = self.parse_icon(parsed)

        normalized_icon_url = normalize_url(parsed_icon, parsed.feed.link)

        feed_meta = FeedMeta(
            title=parsed.feed.title,
            description=self.parse_description(parsed),
            icon_url=normalized_icon_url,
            rss_url=url,
            url=parsed.feed.link,
            entries=parsed.entries,
        )

        yield feed_meta

    def parse_icon(self, parsed: FeedParserDict) -> str:
        if parsed.feed.get('image') is not None:
            return parsed.feed.image.href
        elif parsed.feed.get('icon') is not None:
            return parsed.feed.icon
        elif self.articulo.icon is not None:
            return self.articulo.icon
        # FIXME: this is a small hack to retrieve favicon if there is no favicons
        #  in the head tag. Need to move it to articulo library
        parsed_url = list(urlparse(parsed.feed.link))
        parsed_url[2] = 'favicon.ico'
        return urlunparse(parsed_url)

    def parse_description(self, parsed: FeedParserDict) -> str:
        if parsed.feed.get('description') is not None:
            return parsed.feed.description
        return self.articulo.description


class HTMLFeedParser(RSSFeedParser):
    def parse(self, url: str) -> Generator[FeedMeta]:
        for rss_link in self.articulo.rss:
            normalized_url = normalize_url(rss_link, url)
            return super().parse(normalized_url)


def get_form_parser(content_type, articulo):
    if content_type == FeedContentTypes.TEXT_HTML.value:
        return HTMLFeedParser(articulo)
    return RSSFeedParser(articulo)
