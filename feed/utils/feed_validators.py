from abc import ABC

from articulo import Articulo


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
