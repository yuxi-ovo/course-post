import json
import urllib.request
from datetime import datetime

import redis
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

from src.course.db import addUpdateCourseLog, saveCourse

a = {
    "软件2303班": {
        "第一周": {
            "星期一": {
                "第一大节": {
                    "课程名"
                }
            }
        }
    }
}


def weekSort(arr):
    r = {
        "星期一": {},
        "星期二": {},
        "星期三": {},
        "星期四": {},
        "星期五": {},
        "星期六": {},
        "星期日": {},
    }
    for k in arr:
        r[k] = arr[k]
    return r


def getTemplate(cookie="", template="", user='张瑞'):
    url = 'https://jw.hniu.cn/jsxsd/kbcx/kbxx_xzb_ifr';
    head = {
        "cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    }
    logger.info("封装请求头成功")
    if template != "":
        html = template
    else:
        data = urllib.parse.urlencode({"xnxqh": "2024-2025-1", "kbjcmsid": "67FB3A89FDC146ADA865DCC81B9EC143"}).encode(
            "utf-8")
        request = urllib.request.Request(url, headers=head, method="POST", data=data)
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    courseList = getClass(soup)
    getClassCourse(courseList, soup)
    logger.info("爬取所有班级课表成功")
    courseDataList = []
    classList = []
    for c in tqdm(courseList):
        # 班级
        classList.append((c,))
        for w in courseList[c]:
            # 周次
            courseList[c][w] = weekSort(courseList[c][w])
            for d in courseList[c][w]:
                # 星期
                # print(c, w, d)
                courseData = courseList[c][w][d]
                courseData = json.dumps(courseData, ensure_ascii=False)
                courseDataList.append((c, w, d, courseData))
    if template != "":
        return classList, courseDataList
    else:
        saveCourse(courseDataList, classList)
        addUpdateCourseLog(user)
        logger.info("保存班级课表数据完成!")


def getClass(template):
    tableTrList = template.find("table").findChildren("tr")[2:]
    classList = {}
    for tr in tableTrList:
        className = tr.contents[1].findChildren('nobr')[0].text
        classList[className] = {}
        addClassWeek(classList, className)
    return classList


def addClassWeek(classList, className):
    for i in range(1, 26):
        classList[className]["第{}周".format(i)] = {}


def getClassCourse(courseList, template):
    courseTemplate = template.find("table").findChildren("tr")[2:]
    weekDay = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekDayIndex = 0
    section = ["第一大节", "第二大节", "第三大节", "第四大节", "第五大节", "第六大节"]
    sectionIndex = 0
    for c in courseTemplate:
        courseDataList = c.findChildren("nobr")
        weekDayIndex = 0
        sectionIndex = 0
        for k in courseDataList:
            if len(k.text.strip()) == 0:
                # 无课
                sectionIndex += 1
                if sectionIndex > 5:
                    weekDayIndex += 1
                    sectionIndex = 0
                if weekDayIndex > 6:
                    weekDayIndex = 0
                    sectionIndex = 0
                continue
            elif len(k.text.strip()) <= 15:
                # 名字
                continue
            for course in k.contents:
                if course == '\n':
                    continue
                courseData = str(course).split('<br/>')
                courseName = courseData[0][30:]
                courseClass = courseData[1]
                courseTeacher = courseData[2].split("\n")[1]
                courseWeek = courseData[2].split("\n")[2]
                coursePosition = courseData[3].split("\n")[1]
                courseSection = section[sectionIndex]
                courseWeekDay = weekDay[weekDayIndex]
                courseData = {
                    "courseName": courseName,
                    "courseClass": courseClass,
                    "courseTeacher": courseTeacher,
                    "courseWeek": courseWeek,
                    "coursePosition": coursePosition,
                    "courseSection": courseSection,
                    "courseWeekDay": courseWeekDay
                }
                addWeekCourse(courseList, courseClass, weekDay[weekDayIndex], section[sectionIndex], courseData)
            sectionIndex += 1
            if sectionIndex > 5:
                weekDayIndex += 1
                sectionIndex = 0
            if weekDayIndex > 6:
                weekDayIndex = 0
                sectionIndex = 0


def addWeekCourse(courseList, className, weekDay, section, courseData):
    courseData['courseWeek'] = courseData.get('courseWeek').replace("(", "").replace(")", "")
    weekData = courseData.get('courseWeek').split(",")

    for i in weekData:
        temp = i.split("-")
        if len(temp) != 1:
            minWeek = temp[0].replace("周", "")
            maxWeek = temp[1].replace("周", "")
            addCourse(maxWeek, minWeek, courseList, className, weekDay, section, courseData)
        else:
            if '单' in temp[0]:
                maxWeek = 0
                minWeek = temp[0][0]
                print(minWeek)
                addCourse(maxWeek, minWeek, courseList, className, weekDay, section, courseData)
                continue
            addCourse(0, temp[0].replace("周", ""), courseList, className, weekDay, section, courseData)


def addCourse(maxWeek, minWeek, courseList, className, weekDay, section, courseData):
    maxWeek = int(maxWeek)
    minWeek = int(minWeek)
    week = ''

    def add():
        courseList[className].setdefault(week, {})
        courseList[className][week].setdefault(weekDay, {})
        courseList[className][week][weekDay].setdefault(section, courseData)

    if maxWeek == 0:
        week = "第{}周".format(minWeek)
        add()
    else:
        for i in range(minWeek, maxWeek + 1):
            week = "第{}周".format(i)
            add()


def clearRedis():
    redis_cli = redis.Redis(host='114.132.175.70',  # 服务器公网ip
                            port=6379,  # 服务器Redis端口号
                            db=0,  # 所访问的Redis的数据库编号
                            password=20050703
                            )
    redis_cli.flushdb()
    logger.info("清空redis缓存成功")

    logger.success("更新课表成功！{}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
