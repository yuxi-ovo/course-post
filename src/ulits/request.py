import urllib.request
from typing import Literal

from bs4 import BeautifulSoup
from loguru import logger


def getUrlHtmlContent(url: str, cookie: str, data=None,
                      method: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET') -> BeautifulSoup:
    if data is None:
        data = {}
    if cookie is None:
        raise ValueError("cookie cannot be empty")
    head = {
        "cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    }
    logger.info("封装请求头成功")
    data = urllib.parse.urlencode(data).encode(
        "utf-8")
    request = urllib.request.Request(url, headers=head, method=method, data=data)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup
