from enum import Enum


class FeedContentTypes(Enum):
    TEXT_HTML = 'text/html'
    TEXT_XML = 'text/xml'
    APPLICATION_XML = 'application/xml'
    APPLICATION_XML_RSS = 'application/rss+xml'
    APPLICATION_XML_ATOM = 'application/atom+xml'
