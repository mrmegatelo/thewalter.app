from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen, Request


def get_url_content_type(url):
    req = Request(url, headers={'User-Agent': "Magic Browser"})
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
