from abc import ABC

from articulo import Articulo

from feed.utils.enums import FeedContentTypes
from feed.utils.helpers import get_url_content_type


class AbstractValidator(ABC):
    articulo: Articulo

    def __init__(self, articulo: Articulo):
        self.articulo = articulo

    def validate(self, url: str) -> None | str:
        pass


class RSSLinkValidator(AbstractValidator):
    def validate(self, url):
        return


class HTMLLinkValidator(AbstractValidator):
    def validate(self, url):
        if self.articulo.rss is None:
            return 'This link has no feed.'

        return


def get_form_validator(url, articulo):
    content_type = get_url_content_type(url)
    match content_type:
        case FeedContentTypes.TEXT_HTML.value:
            return HTMLLinkValidator(articulo)
        case (
            FeedContentTypes.TEXT_XML.value
            | FeedContentTypes.APPLICATION_XML.value
            | FeedContentTypes.APPLICATION_XML_RSS.value
            | FeedContentTypes.APPLICATION_XML_ATOM.value
        ):
            return RSSLinkValidator(articulo)
