import requests
from bs4 import BeautifulSoup
from loguru import logger

from src.ulits.cookie import getCookieForServerV2


def getScore(username: str, password: str):
    # 桌面个人课表 https://jw.hniu.cn/jsxsd/framework/main_index_loadkb.htmlx?rq=2024-11-25&sjmsValue=&xnxqid=2024-2025-1
    cookie = getCookieForServerV2(username, password)
    head = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    }
    logger.info("封装请求头成功")
    # data = urllib.parse.urlencode({"xsfs": 'all'}).encode("utf-8")
    scoreList = getAllScore(head)
    return scoreList


def getUnCourse(username: str, password: str):
    cookie = getCookieForServerV2(username, password)
    head = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    }
    logger.info("封装请求头成功")
    # data = urllib.parse.urlencode({"xsfs": 'all'}).encode("utf-8")
    scoreList = getAllScore(head, 4)
    global scoreIndex
    scoreIndex = 0
    return scoreList


def getAllScore(head, Type: int = None):
    scoreList = []
    # 1已修课程 2未及格课程 3选修课 4 未修课程
    if Type is not None:
        html = getScoreHtml(head, str(4))
        soup = BeautifulSoup(html, "html.parser")
        scoreList += analyze(soup)
    else:
        for t in range(1, 4):
            html = getScoreHtml(head, str(t))
            soup = BeautifulSoup(html, "html.parser")
            scoreList += analyze(soup)

    return scoreList


def getScoreHtml(head, type: str):
    url = 'https://jw.hniu.cn/jsxsd/bygl/bygl_ckxsList'
    response = requests.get(url, headers=head, params={'xs0101id': '202315310305', 'type': type})
    html = response.text
    return html


# 课程序号变量
scoreIndex = 1


def analyze(html):
    scoreHtmlList = html.find("table", id='dataList').find_all('tr')[1:]
    # keyMap = ["序号", "开课日期", "课程性质", "课程编号", "课程名字", "成绩", "课程属性", "课程性质2", "课程学分",
    #           "课程学时"]
    keyMap = ["index", "startDate", "nature", "id", "name", "score", "type", "nature2", "credit"]
    keyIndex = 0
    scoreList = []
    global scoreIndex
    for row in scoreHtmlList:
        data = row.find_all('td')
        scoreData = {}
        for d in data:
            key = keyMap[keyIndex]
            if key == '序号':
                scoreData[key] = scoreIndex
                scoreIndex += 1
            else:
                scoreData[key] = d.get_text()
            keyIndex += 1
            if keyIndex >= len(keyMap):
                keyIndex = 0
        scoreList.append(scoreData)
    scoreIndex = 0
    return scoreList


if __name__ == '__main__':
    getScore("202315310305", "20050703zrZR")
