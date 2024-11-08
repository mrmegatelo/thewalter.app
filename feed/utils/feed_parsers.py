from collections.abc import Generator
from urllib.parse import urlparse, urlunparse
from abc import ABC, abstractmethod
from dataclasses import dataclass

import feedparser
from articulo import Articulo
from feedparser import FeedParserDict


@dataclass
class FeedMeta:
    title: str
    description: str
    icon_url: str
    rss_url: str
    url: str

class AbstractFeedParser(ABC):

    articulo: Articulo

    def __init__(self, articulo: Articulo):
        self.articulo = articulo

    @abstractmethod
    def parse(self, url: str) -> FeedMeta:
        pass


class RSSFeedParser(AbstractFeedParser):
    def parse(self, url: str) -> Generator[FeedMeta]:
        parsed = feedparser.parse(url)
        feed_meta = FeedMeta(
            title=parsed.feed.title,
            description=self.parse_description(parsed),
            icon_url=self.parse_icon(parsed),
            rss_url=url,
            url=parsed.feed.link,
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
            return super().parse(rss_link)