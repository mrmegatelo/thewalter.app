from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen, Request


def get_url_content_type(url):
    req = Request(url, headers={'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"})
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
