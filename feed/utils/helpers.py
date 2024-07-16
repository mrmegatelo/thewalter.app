from urllib.request import urlopen, Request


def get_url_content_type(url):
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    res = urlopen(req)
    http_message = res.info()
    return http_message.get_content_type()
