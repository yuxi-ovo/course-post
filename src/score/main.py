import requests
from bs4 import BeautifulSoup
from loguru import logger

from src.ulits.cookie import getCookieForServer


def getScore(username: str, password: str):
    url = 'https://jw.hniu.cn/jsxsd/kscj/cjcx_list'
    # 桌面个人课表 https://jw.hniu.cn/jsxsd/framework/main_index_loadkb.htmlx?rq=2024-11-25&sjmsValue=&xnxqid=2024-2025-1
    cookie = getCookieForServer(username, password)
    head = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    }
    logger.info("封装请求头成功")
    # data = urllib.parse.urlencode({"xsfs": 'all'}).encode("utf-8")
    response = requests.post(url, headers=head)
    print("html", response)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    scoreList = analyze(soup)
    return scoreList


def analyze(html):
    table = html.find("table", id='dataList').findAll('tr')
    scoreList = []
    for i in range(1, len(table)):
        name = table[i].findAll("td")[3].text.strip()
        value = table[i].findAll("td")[4].text.strip()
        scoreList.append({'name': name, 'value': value})
    return scoreList


if __name__ == '__main__':
    getScore("202315310305", "20050703zrZR")
